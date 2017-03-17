# wechat-wci-spider

抓取搜狗微信搜索引擎微信公众号传播力WCI项目，提供代理ip。支持py2和py3两个版本。
<br/>
详细使用方式:<br/>
配置proxypool下的数据库配置以及自定义常量，相关配置请参考[IPProxyPool](https://github.com/qiyeboy/IPProxyPool)<br/>
配置config.json 数据库相关配置以及搜狗通行证账号密码以及要抓取的微信公众号<br/>
由于项目用到selenium,请前往[下载](http://chromedriver.storage.googleapis.com/index.html)Chromedriver并配置到环境变量，版本根据自己chrome浏览器版本配置，建议使用2.6版本<br/>
配置完成打开proxypool，python IPProxy.py 启动代理池；然后python wechat.py启动爬虫
<br/>
感谢[qiyeboy](https://github.com/qiyeboy/IPProxyPool)开源的代理池项目。
<br/>
##项目依赖
####Ubuntu,debian
<br/>
1.安装sqlite数据库(一般系统内置):
apt-get install sqlite3
<br/>
2.安装requests,chardet,web.py,gevent,bs4,selenium:
pip install requests chardet web.py sqlalchemy gevent bs4 selenium
<br/>
3.安装lxml:
apt-get install python-lxml
<br/>
注意：

* python3下的是pip3
* 有时候使用的gevent版本过低会出现自动退出情况，请使用pip install gevent --upgrade更新)
* 在python3中安装web.py，不能使用pip，直接下载py3版本的[源码](https://codeload.github.com/webpy/webpy/zip/py3)进行安装

####Windows
1.下载[sqlite](http://www.sqlite.org/download.html),路径添加到环境变量
<br/>
2.安装requests,chardet,web.py,gevent,bs4,selenium:
pip install requests chardet web.py sqlalchemy gevent
<br/>
3.安装lxml:
pip install lxml或者下载[lxml windows版](https://pypi.python.org/pypi/lxml/)
<br/>
注意：

* python3下的是pip3
* 有时候使用的gevent版本过低会出现自动退出情况，请使用pip install gevent --upgrade更新)
* 在python3中安装web.py，不能使用pip，直接下载py3版本的[源码](https://codeload.github.com/webpy/webpy/zip/py3)进行安装

####扩展说明
本项目默认数据库是sqlite，但是采用sqlalchemy的ORM模型，通过预留接口可以拓展使用MySQL，MongoDB等数据库。
配置方法：
<br/>
1.MySQL配置
```
第一步：首先安装MySQL数据库并启动
第二步：安装MySQLdb或者pymysql(推荐)
第三步：在config.py文件中配置DB_CONFIG。如果安装的是MySQLdb模块，配置如下：
        DB_CONFIG={
            'DB_CONNECT_TYPE':'sqlalchemy',
            'DB_CONNECT_STRING':'mysql+mysqldb://root:root@localhost/proxy?charset=utf8'
        }
        如果安装的是pymysql模块，配置如下：
         DB_CONFIG={
            'DB_CONNECT_TYPE':'sqlalchemy',
            'DB_CONNECT_STRING':'mysql+pymysql://root:root@localhost/proxy?charset=utf8'
        }
```
sqlalchemy下的DB_CONNECT_STRING参考[支持数据库](http://docs.sqlalchemy.org/en/latest/core/engines.html#supported-databases)，理论上使用这种配置方式不只是适配MySQL，sqlalchemy支持的数据库都可以，但是仅仅测试过MySQL。
<br/>
2.MongoDB配置
```
第一步：首先安装MongoDB数据库并启动
第二步：安装pymongo模块
第三步：在config.py文件中配置DB_CONFIG。配置类似如下：
        DB_CONFIG={
            'DB_CONNECT_TYPE':'pymongo',
            'DB_CONNECT_STRING':'mongodb://localhost:27017/'
        }
```
由于sqlalchemy并不支持MongoDB,因此额外添加了pymongo模式，DB_CONNECT_STRING参考pymongo的连接字符串。
#####注意
如果大家想拓展其他数据库，可以直接继承db下ISqlHelper类，实现其中的方法，具体实现参考我的代码，然后在DataStore中导入类即可。
```
try:
    if DB_CONFIG['DB_CONNECT_TYPE'] == 'pymongo':
        from db.MongoHelper import MongoHelper as SqlHelper
    else:
        from db.SqlHelper import SqlHelper as SqlHelper
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
except Exception,e:
    raise Con_DB_Fail
```


## 如何使用

将项目目录clone到当前文件夹

$ git clone

切换工程目录

```
$ cd wechat-wci-spider/proxypool
```

运行代理池脚本

```
python IPProxy.py
```
成功运行后，打印信息
```
IPProxyPool----->>>>>>>>beginning
http://0.0.0.0:8000/
IPProxyPool----->>>>>>>>db exists ip:0
IPProxyPool----->>>>>>>>now ip num < MINNUM,start crawling...
IPProxyPool----->>>>>>>>Success ip num :134,Fail ip num:7882
```
运行爬虫脚本
```
cd ..
```

```
python wechat.py
```
成功运行后，自动打开浏览器登录sogou,并打印抓取信息
```
http://weixin.sogou.com/weixin?type=2&ie=utf8&tsn=5&interation=null&from=tool&usip=sqgxyxmt&wxid=oIWsFtwSrbd-iUQ6MI2bWeQT3LB0&query=sqgxyxmt&ft=2016-12-01&et=2016-12-31
27
http://weixin.sogou.com/weixin?type=2&ie=utf8&tsn=5&interation=null&from=tool&usip=sqgxyxmt&wxid=oIWsFtwSrbd-iUQ6MI2bWeQT3LB0&query=sqgxyxmt&ft=2016-12-01&et=2016-12-31&page=1
<p class="txt-info" id="sogou_vr_11002601_summary_0">为进一步加强现代大学生对新媒体的认识与了解,跟进时代的步伐,商丘工学院于2016年12月2日在生活区广场举行了商丘工学院十佳...</p>
<p class="txt-info" id="sogou_vr_11002601_summary_1" style="display:none">爱心募捐,商丘工学院在行动】在听闻小梦冉事件后,商丘工学院公寓自律委员会和新媒体联盟携手发起为曹梦冉小姑娘募捐活动,...</p>
<p class="txt-info" id="sogou_vr_11002601_summary_2">深化“两学一做”学习教育  让党旗在民办高校高高飘扬——党委书记刘兵为全校党务工作者和师生党员上党课12月8日晚,党委书记刘...</p>
<p class="txt-info" id="sogou_vr_11002601_summary_3">为进一步加强我校学生干部队伍建设,提高学生干部的品德修养和综合素质.11月30日晚,商丘工学院“青年马克思主义培养工程”...</p>
<p class="txt-info" id="sogou_vr_11002601_summary_4">12月8日下午,商丘工学院校长李纪轩教授在明德讲堂作了题为“《老子》的人生智慧”专题讲座.副校长王峰、范玉峰,二级学院(...</p>
<p class="txt-info" id="sogou_vr_11002601_summary_5" style="display:none">12月21日晚,由学生事务服务中心主办,医学院承办,中国移动商丘分公司协办的商丘工学院第六届“移动杯”辅导员职业能力大赛闭...</p>
<p class="txt-info" id="sogou_vr_11002601_summary_6">12月28日下午,由安阳师范学院副校长张建国任组长,河南中医药大学保卫处处长刘明、安阳师范学院科长苗安民为成员的河南省高校...</p>
<p class="txt-info" id="sogou_vr_11002601_summary_7">12月8日中午,商丘工学院新媒体联盟暨校院两级党委系统学生组织聘书颁发仪式在明德讲堂举行.校长助理刘永福出席了此次会议,...</p>
<p class="txt-info" id="sogou_vr_11002601_summary_8">捡到笔记本电脑 保洁员等了四小时校方发动师生在全校寻找失主,次日终于完璧归赵晚报记者 成绍峰 来源:商丘网—京九晚报 11月29...</p>
<p class="txt-info" id="sogou_vr_11002601_summary_9">来源:人民日报【商丘工学院“法制知多少”校园采访】在全国法制宣传日即将到来之际,为增强广大学生的法律意识和法治观念,巩...</p>
http://weixin.sogou.com/weixin?type=2&ie=utf8&tsn=5&interation=null&from=tool&usip=sqgxyxmt&wxid=oIWsFtwSrbd-iUQ6MI2bWeQT3LB0&query=sqgxyxmt&ft=2016-12-01&et=2016-12-31&page=2
<p class="txt-info" id="sogou_vr_11002601_summary_0" style="display:none">崔国莲介绍2012年06月至2013年11月  园林设计师 内蒙古绿华园林工程有限公司参与项目:1.敕勒川草原文化旅游区草原部落景观设...</p>

```

## 使用说明


该项目用于采集公众号每个月的微信影响力指数，所以结果是按月来的，如有别的需求请自行修改。<br/>
cookies失效会自动打开浏览器登录获得cookies，所以会不定时打开网页并自动关闭，这个是正常现象。

## TODO
1.代码执行效率太低，考虑下一步使用多进程以及协程
<br/>


## 更新进度


-----------------------------2017-3-17----------------------------
<br/>
1.初始化项目
<br/>
