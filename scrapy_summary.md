# python scrapy框架

## 其他技能

```shell
    1.从 settings.py 中取相关的参数的值
            注意到 各个类的__init__中的第二个参数 与 @classmethod 中 return 值
            (1) 方法一  
                 class MysqlTwistedPipeline(object):

                    def __init__(self, dbpool):
                        self.dbpool = dbpool
                        
                    @classmethod
                    # 这里的 settings 就是对应于 settings.py 中 相关的数据库参数
                    def from_settings(cls, settings): 
                        database=settings["MYSQL_DBNAME"]
                        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
                        return cls(dbpool)   
                    
            (2) 方法二
                       class UserAgentMiddleware(object):
                        def __init__(self, user_agent='Scrapy'):
                            self.user_agent = user_agent
                    
                        @classmethod
                        def from_crawler(cls, crawler):
                            return cls(crawler.settings['USER_AGENT'])
                            
            
                                
```
 
## pyhton scrapy 整体布局

```shell
    1.scrapy 框架组件
        (1) Spiders
        (2) Item Pipeline
        (3) Scheduler
        (4) Downloader
        (5) Scrapy Engine
        
    2.流程
        所有的 Request,Response 的数据都要通过 Scrapy Engine.
        Spider 发送了一个 Request 给 Scrapy Engine, Scrapy Engine拿到之后直接给 Scheduler,
        同时 Scheduler 经过调度 生成 Request 给 Scrapy Engine, Scrapy Engine 再经过
        Downloader Middleware 一层一层得过滤 再传给 DownLoader, DownLoader在下载完成之后
        再通过 配置好的 一层一层Downloader Middleware, 发送给 Scrapy Engine, Scrapy Engine
        拿到 http response 后 在返回给 Spider, Spider 就可以做一些处理, 比如Spider解析出 item
        或则 其他的 requests,  再传输给 Scrapy Engine , Scrapy Engine 进行判断如果是item,则
        交给 Item Pipeline进行处理.如果是新的Request,则 重新按第一步来做.
        
    3. 源码
          (1) 在 site-packages\scrapy\core\engine.py
              A. 第一个重要的函数 schedule
                class ExecutionEngine(object):
                   def schedule(self, request, spider):
                        self.signals.send_catch_log(signal=signals.request_scheduled,
                                request=request, spider=spider)
                        if not self.slot.scheduler.enqueue_request(request):
                            self.signals.send_catch_log(signal=signals.request_dropped,
                                                        request=request, spider=spider)
                                                                
                当 Scrapy Engine 收到 Spider 的Request 请求时, 会调用 ExecutionEngine.schedule,
                此时 会调用 类Scheduler中的enqueue_request
                      class Scheduler(object): 
                        def enqueue_request(self, request):
                            if not request.dont_filter and self.df.request_seen(request):
                                self.df.log(request, self.spider)
                                return False
                            dqok = self._dqpush(request)
                            if dqok:
                                self.stats.inc_value('scheduler/enqueued/disk', spider=self.spider)
                            else:
                                self._mqpush(request)
                                self.stats.inc_value('scheduler/enqueued/memory', spider=self.spider)
                            self.stats.inc_value('scheduler/enqueued', spider=self.spider)
                            return True
                            
                     这个方法就是将收到的Request 放到 Schedule 中
                     
              B. 第二个重要的函数 _next_request_from_scheduler
              class ExecutionEngine(object):
                  def _next_request_from_scheduler(self, spider):
                    slot = self.slot
                    request = slot.scheduler.next_request()
                    if not request:
                        return
                    d = self._download(request, spider)
                    d.addBoth(self._handle_downloader_output, request, spider)
                    d.addErrback(lambda f: logger.info('Error while handling downloader output',
                                                       exc_info=failure_to_exc_info(f),
                                                       extra={'spider': spider}))
                    d.addBoth(lambda _: slot.remove_request(request))
                    d.addErrback(lambda f: logger.info('Error while removing request from slot',
                                                       exc_info=failure_to_exc_info(f),
                                                       extra={'spider': spider}))
                    d.addBoth(lambda _: slot.nextcall.schedule())
                    d.addErrback(lambda f: logger.info('Error while scheduling new request',
                                                       exc_info=failure_to_exc_info(f),
                                                       extra={'spider': spider}))
                    return d
                    
              要向 DownLoader 发送的 Request 是从 Scheduler 中取
              
          (2) 在site-packages\scrapy\core\downloader\handlers目录下 有 file.py, ftp.py, http.py
              所以其支持很多下载方式,
              
          (3) site-packages\scrapy 目录的组织结构:
                A. commands : 命令相关的
                B. contracts: 关于测试
                C. contrib:   
```

## scrapy 2个重要的类

### 简介

```shell
    1.Request对象 是由 Spider 组件产生的, Response 对象 是由 DownLoader 组件 产生的
      Spider 组件 yield Request 给 Scrapy Engine 组件, Scrapy Engine 组件 压入到 Schedule
      DownLoader 组件下载完成后 将 Response 返回给 Scrapy Engine, Scrapy Engine 在交给 Spider``
```

### Request

```shell
    (1) 构造函数
             class Request(object_ref):
        
            def __init__(self, url, callback=None, method='GET', headers=None, body=None,
                         cookies=None, meta=None, encoding='utf-8', priority=0,
                         dont_filter=False, errback=None, flags=None):
                         
            cookies : 在登录之后 scrapy 自动将我们的 cookies 加入到 Request 中, 其实现方式是： 在scrapy
                      中\site-packages\scrapy\downloadermiddlewares\cookies.py , cookies.py 里面
                      有 类 class CookiesMiddleware(object) 这里实现了 cookies的填充, 
                      
            meta: 我们想在 Request 和 response 之间添加额外的信息， 可以进行额外的参数传递
            encoding: 我们的网页可以设置字符编码, 一般的网页设置的是 utf-8编码
            priority : 这个参数会影响 Schedule 的优先调度, 在某些情况下当我们想要将某些 Request优先发送时
                       the priority of this request (defaults to 0). The priority is used by 
                       the scheduler to define the order used to process requests. 
                       Requests with a higher priority value will execute earlier.
                       
            dont_filter: 设置为 False 时表明 这个Request 不应该被 Schedule 过滤, 
            errback： 错误的回调函数, 例如 当 response为 404 的时候, 就会调用这个回调函数进行处理
```

### Response

```shell
    1.位置
         site-packages\scrapy\http\response\__init__.py
         
    2.
        class Response(object_ref):
            def __init__(self, url, status=200, headers=None, body=b'',
                         flags=None, request=None):
                         
        Response.status: 代表页面返回的状态     
        Response.headers ： 服务器放回的headers    
        Response.body: http 返回的内容  
        Response.request ： 之前 yield 的 Request对象
        
    3.继承于Response对象的 HtmlResponse 类
         A. 位置 site-packages\scrapy\http\response\html.py
                class HtmlResponse(TextResponse):
                
                class TextResponse(Response):
                    _DEFAULT_ENCODING = 'ascii'
                
                    def __init__(self, *args, **kwargs):
                        self._encoding = kwargs.pop('encoding', None)
                        self._cached_benc = None
                        self._cached_ubody = None
                        self._cached_selector = None
                        super(TextResponse, self).__init__(*args, **kwargs)
                2个重要的方法:       
                        def xpath(self, query, **kwargs):
                            return self.selector.xpath(query, **kwargs)

                        def css(self, query):
                            return self.selector.css(query)         
```

## 如何随机的更换 user-agent

```shell
    1.简介
        User_agent 是用户代理,  向服务器请求数据时用来标识自己
        
    2.随机的更换user_agent
        根据 scrapy 框架 每次Request 请求 都会由 Scrapy Engine组件 通过  downloder-middleware 传给 DownLoader
        组件, 所以可以在 downloader-middleware 中 随机更换 user-agent. 
        A.
            scrapy 框架本身提供了一个downLoader-middleware 下的随机更换user-agent的文件 
                site-packages\scrapy\downloadermiddlewares\useragent.py, 
                    class UserAgentMiddleware(object):
                    """
                     This middleware allows spiders to override the user_agent
                    """
        
                        def __init__(self, user_agent='Scrapy'):
                            self.user_agent = user_agent
                    
                        @classmethod
                        def from_crawler(cls, crawler):
                            o = cls(crawler.settings['USER_AGENT']) 
                            crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
                            return o
                            
                        其中 crawler.settings['USER_AGENT'] 代表是在settings.py 定义的 USER_AGENT 的值
                        
                         def process_request(self, request, spider):
                            if self.user_agent:
                                request.headers.setdefault(b'User-Agent', self.user_agent)
                                
                         process_request函数是将从 settings.py 得到的 USER_AGENT, 对Request中的 headers进行赋值.
                        
                操作
                    在settings.py
                        USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64)" \
                                     " AppleWebKit/537.36 (KHTML, like Gecko) " \
                                     "Chrome/63.0.3239.108 Safari/537.36"
                                     
        B.
            如何来写一个自己定义的 middleware
            第一步:
                在 settings.py 文件定义
                    DOWNLOADER_MIDDLEWARES = {
                       'ArticleSpider.middlewares.ArticlespiderDownloaderMiddleware': 543,
                        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                    }
                          
                    如果要将scrapy 框架中 内置的 UserAgentMiddleware disable掉, 则令其值为 None      
                    注意: 对应的值(543)越大, 其对应的函数越晚被执行。
                    
            第二步:
                安装 fake-useragent(github有该项目) 用于方便应用 Request.headers 中的User-agent,
                随机取各个浏览器的User-agent
                D:\python_example\ArticleSpider (master -> origin)
                    (article_spider) > pip install fake-useragent
                    
                对应的url: https://fake-useragent.herokuapp.com/browsers/0.1.4  其中0.1.4是对应的版本号
                可以通过 D:\python_example\ArticleSpider (master -> origin)
                        (article_spider) > pip list
                        结果:
                            fake-useragent   0.1.10 
                            https://fake-useragent.herokuapp.com/browsers/0.1.10 不一定有
                            
            第三步:
                (1) 在ArticleSpider\middlewares.py  自定义 DownLoader-middleware
                
                    from fake_useragent import UserAgent
                    
                    """
                       随机更换 User-agent
                    """
                    
                    class RandomUserAgentMiddleware(object):
                    
                        def __init__(self, crawler):
                            super(RandomUserAgentMiddleware, self).__init__()
                            """
                                定义第三方模块 UserAgent对象, 
                                通过调用 self.ua.random 方法取随机浏览器的User-agent
                                通过调用 self.ua.google 方法去google浏览器的随机User-agent
                            """
                            self.ua = UserAgent()
                            """
                               通过 crawler 对象可以从 setting.py文件中取一些定义的参数
                            """
                            self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")
                    
                        """
                         将 crawler 对象传递到 RandomUserAgentMiddleware类中
                        """
                        @classmethod
                        def from_crawler(cls, crawler):
                            return cls(crawler)
                    
                        def process_request(self, request, spider):
                            """
                                通过 getattr()方法 得到
                                self.ua.random,self.ua.google 这取决于 self.ua_type 的值
                            """
                            def get_ua():
                                return getattr(self.ua, self.ua_type)
                            request.headers.setdefault('User-Agent', get_ua())
                            
                            """
                                设置 ip 代理, 隐藏本机的ip,不会被服务器封
                            """
                            request.meta["proxy"] = "http://125.118.247.4:6666"
                            
                (2) 在 settings.py 定义变量
                        RANDOM_UA_TYPE = "random"
                        
            第四步:
                在 settings.py 中 将 RandomUserAgentMiddleware 类加入到DOWNLOADER_MIDDLEWARES中
                    DOWNLOADER_MIDDLEWARES = {
                       'ArticleSpider.middlewares.RandomUserAgentMiddleware': 543,
                        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                    }
```

## 如何设置 ip 代理

```shell
    1.ip 的变化策略, 如果爬取访问频率过快, 本机的ip将会被禁, 这时候可以采取 重启路由器方法(不一定有效)
    2.ip 代理
        (1) 首先浏览器向 代理服务器发起请求(要获取伯乐在线的数据), 然后 代理服务器 再向伯乐在线请求数据, 返回
            数据response先到 代理服务器, 代理服务器再到 浏览器
        (2) 通过 西刺免费代理IP 可以拿到 高匿IP代理 IP:port
        (3) scrapy框架设置 IP代理
                """
                    设置 ip 代理, 隐藏本机的ip,不会被服务器封
                """
                request.meta["proxy"] = "http://125.118.247.4:6666"
                
    3.如果构建 IP 代理池
        第一步:
                先向 西刺免费代理IP 网站进行爬取 高匿IP 的信息, 存入到数据库中
        
```