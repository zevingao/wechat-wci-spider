#coding=utf8
from selenium import webdriver
import json , calendar
import requests
import sys,bs4,threading
import re,time
import random , datetime ,math , pymysql
requests.adapters.DEFAULT_RETRIES = 5
reload(sys)
sys.setdefaultencoding('utf8')
class Crawl:

    __startUrl = "http://weixin.sogou.com/weixin?type=2&ie=utf8&tsn=5&interation=null&from=tool"
    __getWxIdApi = "http://weixin.sogou.com/weixin?zhnss=1&type=1&ie=utf8&query="
    __dbProxyApi = 'http://127.0.0.1:8000/?types=0&count=100&country=%E5%9B%BD%E5%86%85'
    __contApi = 'http://mp.weixin.qq.com/mp/getcomment'
    __wechatId = ''
    __wechatIdCopy = ''
    __wxName = ''
    __startTime = ''
    __endTime = ''
    __crawlUrl = ''
    __dbhost = ''
    __dbuser = ''
    __dbpwd = ''
    __dbname= ''
    __sogouName = ''
    __sogouPwd = ''
    __spaceTime = 10
    __year = 2016
    __totalPage = 0
    __totalNum = 0
    __liked = 0
    __readed = 0
    __topReaded = 0
    __topLiked = 0
    __highRead = 0
    __urlList = []
    __session = ''
    __proxy = []
    __cookies = {}
    __dates = {}
    __proxies = {}
    __task = []
    __result = []
    __getCookiesTimes = 0
    __timers = []

    def __init__(self):
        self.__session = requests.session()
        self.__session.keep_alive = False
        self.getDbProxy()
        self.getSettings()
        self.getMonths()
        self.__conn = pymysql.connect(host=self.__dbhost, user=self.__dbuser, passwd=self.__dbpwd, db=self.__dbname, charset='utf8')
        self.__cursor = self.__conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.__proxies['http'] = random.choice(self.__proxy)
        tmp = {}
        tmp['http'] = random.choice(self.__proxy)
        self.__proxies = tmp
        print self.__proxies
        self.checkCookies()
        if self.__startTime != '' and self.__endTime != '':
        	self.__crawlUrl += '&ft=' + self.__startTime + '&et=' + self.__endTime
        print self.__crawlUrl

    def myRequest(self , url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36' , 'Host' : 'weixin.sogou.com' , 'Upgrade-Insecure-Requests' : '1'}
        while True:
			try:
				content = self.__session.get(url, proxies=self.__proxies, headers=headers, cookies=self.__cookies,timeout=2).content
			except Exception as e:
				print 'proxy error' + str(self.__proxies)
				print e
				self.__proxy.remove(self.__proxies['http'])
				if len(self.__proxy) < 10:
					self.getDbProxy()
				temp = random.choice(self.__proxy)
				self.__proxies['http'] = temp
				time.sleep(1)
				continue
			else:
				return content
				break


    def run(self):
        for it in self.__task:
			self.__result = []
			self.__wechatId = it[0]
			self.__wechatIdCopy = it[1]
			wxId = self.getWxId()
			for (k, v) in self.__dates.items():
				temp = str(k)
				if len(temp) == 1:
					temp = '0' + str(temp)
				self.__startTime = str(self.__year) + '-' + temp + '-01'
				self.__endTime = str(v)
				self.rush(k , wxId)
			insertList = []
			for item in self.__result:
				temp = (item['year'], item['month'], item['wxid'], item['wxname'], item['nums'], item['highread'],
						item['totalread'], item['averead'], item['totalliked'], item['topread'], item['aveliked'],
						item['topliked'], item['likedrate'], item['wci'])
				insertList.append(temp)
			res = self.__cursor.executemany("insert into posts_0317(year , month , wxid , wxname , nums , highread , totalread , averead , totalliked , topread , aveliked , topliked , likedrate , wci) values(%s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s)",insertList)
			self.__conn.commit()
        self.__cursor.close()
        print '结束时间:'
        print time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))


    def rush(self , month , wxId):
		self.__totalNum = 0
		self.__liked = 0
		self.__readed = 0
		self.__topReaded = 0
		self.__topLiked = 0
		self.__highRead = 0
		self.__urlList = []
		self.__totalNum = 0
		self.__wxName = ''
		self.__crawlUrl = self.__startUrl + '&usip=' + self.__wechatIdCopy + '&wxid=' + wxId + '&query=' + self.__wechatId
		self.__crawlUrl += '&ft=' + self.__startTime + '&et=' + self.__endTime
		print self.__crawlUrl
		self.getTotalPage()
		self.crawling()
		print len(self.__urlList)
		self.crawlWci()
		temp = {}
		if self.__readed > 0:
			temp['year'] = self.__year
			temp['month'] = month
			temp['wxid'] = self.__wechatId
			temp['wxname'] = self.__wxName
			temp['nums'] = self.__totalNum
			temp['highread'] = self.__highRead
			temp['totalread'] = self.__readed
			temp['averead'] = int(self.__readed / self.__totalNum)
			temp['totalliked'] = self.__liked
			temp['topread'] = self.__topReaded
			temp['aveliked'] = int(self.__liked / self.__totalNum)
			temp['topliked'] = self.__topLiked
			temp['likedrate'] = round(float(self.__liked) / self.__readed, 4)
			time = datetime.datetime.strptime(self.__endTime, '%Y-%m-%d') - datetime.datetime.strptime(self.__startTime,
																									   '%Y-%m-%d')
			a = math.log(self.__readed / time.days + 1, math.e) * 0.4 + 0.45 * math.log(
				self.__readed / self.__totalNum + 1, math.e) + 0.15 * math.log(self.__topReaded + 1, math.e)
			b = 0.4 * math.log(self.__liked / time.days * 10 + 1, math.e) + 0.45 * math.log(
				self.__liked / self.__totalNum * 10 + 1, math.e) + 0.15 * math.log(self.__topLiked * 10 + 1, math.e)
			temp['wci'] = round((a * 0.8 + b * 0.2) ** 2 * 10, 2)
		else:
			temp['year'] = self.__year
			temp['month'] = month
			temp['wxid'] = self.__wechatId
			temp['wxname'] = self.__wxName
			temp['nums'] = self.__totalNum
			temp['highread'] = self.__highRead
			temp['totalread'] = self.__readed
			temp['averead'] = 0
			temp['totalliked'] = self.__liked
			temp['topread'] = self.__topReaded
			temp['aveliked'] = 0
			temp['topliked'] = self.__topLiked
			temp['likedrate'] = 0
			temp['wci'] = 0
		self.__result.append(temp)


    def checkCookies(self):
        print '正在更换cookies...................................................................'
        self.__getCookiesTimes += 1
        if self.__getCookiesTimes > 1:
            self.__timers.append(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time())))
            time.sleep(self.__spaceTime)
        if self.__getCookiesTimes > 30:
			print self.__timers
			time.sleep(60 * 30)
        url = 'https://account.sogou.com/web/webLogin'
        driver = webdriver.Chrome()
        driver.get(url)
        driver.find_element_by_name('username').send_keys(self.__sogouName)
        driver.find_element_by_name('password').send_keys(self.__sogouPwd)
        time.sleep(1)
        driver.find_element_by_tag_name('button').click()
        time.sleep(2)
        driver.get('http://weixin.sogou.com/weixin?type=2&ie=utf8&tsn=5&interation=null&from=tool&usip=北京大学&wxid=oIWsFt0Qd1ojdvW2LUU2QoPUuxrM&query=北京大学&ft=2016-01-01&et=2017-01-01&page=2')
        time.sleep(2)
        print driver.get_cookies()
        cookies = {}
        for item in driver.get_cookies():
            cookies[item["name"]] = item["value"]
        self.__cookies = cookies
        driver.quit()
        return



    def getSettings(self):
        f = open("config.json", 'r')
        settings = json.load(f)
        self.__year = settings['year']
        self.__dbhost = settings['DBHost']
        self.__dbuser = settings['DBUsername']
        self.__dbpwd = settings['DBPwd']
        self.__dbname = settings['DBName']
        self.__spaceTime = settings['spaceTime']
        self.__sogouName = settings['sogouName']
        self.sogouPwd = settings['sogouPwd']
        for x in settings['wxId']:
            self.__task.append(x)


    def getMonths(self):
        for x in xrange(1, 13):
            days = calendar.monthrange(self.__year, x)[1]
            temp = str(x)
            if len(temp) == 1:
                temp = '0' + str(temp)
            self.__dates[x] = str(self.__year) + '-' + temp + '-' + str(days)
        return

    def getSee(self):
    	if self.__urlList:
    		self.__totalNum = len(self.__urlList)
    		for x in self.__urlList:
    			url = x.replace('mp.weixin.qq.com/s?src' , 'mp.weixin.qq.com/mp/getcomment?src')
    			json = self.getContent(url)
    			readed = eval(json)['read_num']
    			liked = eval(json)['like_num']
    			if int(readed) >= 100000:
    				self.__highRead += 1
    			if readed > self.__topReaded:
    				self.__topReaded = readed
    			if liked > self.__topLiked:
    				self.__topLiked = liked
    			self.__readed += readed
    			self.__liked += liked

    def crawlWci(self):
        if self.__urlList:
            th = threading.Thread(target=self.getSee)
            th.start()
            th.join()
        return

    def getContent(self , url):
		while True:
			try:
				try:
					cont = requests.get(url).content
				except Exception as e:
					cont = requests.get(url, proxies=self.__proxies).content
			except Exception as e:
				print 'proxy error getContent' + str(self.__proxies)
				self.__proxy.remove(self.__proxies['http'])
				if len(self.__proxy) < 10:
					self.getDbProxy()
				temp = random.choice(self.__proxy)
				self.__proxies['http'] = temp
				time.sleep(2)
				continue
			else:
				return cont
				break

    def getWxId(self):
    	url = self.__getWxIdApi + self.__wechatId
        while True:
            try:
                try:
                    wxId = eval(requests.get(url).content)['openid']
                except Exception as e:
                    wxId = eval(requests.get(url , proxies = self.__proxies).content)['openid']
            except Exception as e:
                print 'proxy error wxid' + str(self.__proxies)
                self.__proxy.remove(self.__proxies['http'])
                if len(self.__proxy) < 10:
                    self.getDbProxy()
                temp = random.choice(self.__proxy)
                self.__proxies['http'] = temp
                time.sleep(2)
                continue
            else:
                return wxId
                break

    def crawling(self):
		for x in xrange(1 , self.__totalPage + 1):
			url = self.__crawlUrl + '&page=' + str(x)
 			print url
			cont = self.myRequest(url)
			while(self.checkCaptcha(cont) == False):
				print '出现验证码啦！！！！！！！！！！！'
				self.checkCookies()
				temp = random.choice(self.__proxy)
				self.__proxies['http'] = temp
				cont = self.myRequest(url)
			self.crawlInfo(cont)
			time.sleep(self.__spaceTime)

    def crawlInfo(self , content):
    	if content:
    		soup = bs4.BeautifulSoup(content, 'html.parser', from_encoding='gb18030')
	    	strs = soup.select('.txt-box')
	    	if strs:
	    		for x in strs:
    				temp = re.compile(r'href="(.*?)"').findall(x.prettify())[0].encode('utf-8').replace('amp;' , '')
    				self.__urlList.append(temp)
    				keyTemp = x.select('.txt-info')[0]
    				print keyTemp
			soupNow = bs4.BeautifulSoup(content, 'html.parser', from_encoding='gb18030')
			strsNow = soupNow.select('.account')
			if strsNow:
				temp = re.compile(r'>(.*?)</a>').findall(str(strsNow[0]))[0]
				self.__wxName = temp
			else:
				self.__wxName = ''
		else:
			print content


    def getTotalPage(self):
        content = self.myRequest(self.__crawlUrl)
        while (self.checkCaptcha(content) == False):
            print 'totalPage出现验证码啦！！！！！！！！！！！！'
            self.checkCookies()
            temp = random.choice(self.__proxy)
            self.__proxies['http'] = temp
            content = self.myRequest(self.__crawlUrl)
    	soup = bs4.BeautifulSoup(content, 'html.parser', from_encoding='gb18030')
    	strs = soup.select('.mun')
    	if not strs:
    		self.__totalPage = 1
    		return;
    	strs = soup.select('.mun')[0].encode('utf-8')
    	reg = re.compile(r'resultbarnum:(.+?)--')
    	totalNum = re.findall(reg , strs)[0]
    	print totalNum
    	tmp = int(totalNum) % 10
    	self.__totalPage = int(totalNum) / 10 if tmp == 0 else int(totalNum) / 10 + 1

    def checkCaptcha(self , content):
        soup = bs4.BeautifulSoup(content, 'html.parser', from_encoding='gb18030')
        strs = soup.select('.s1')
        if strs:
            temp = re.compile(r'>(.*?)</span>').findall(str(strs[0]))[0]
            if temp == '您的访问出错了':
                print content
                return False
            else:
                return True
        else:
            return True



    def getDbProxy(self):
		jsons = requests.get(self.__dbProxyApi).content
		res = json.loads(jsons)
		for i in res:
			s = str(i[0]) + ':' + str(i[1])
			self.__proxy.append(s)


if __name__ == '__main__':
	crawl = Crawl()
	crawl.run()