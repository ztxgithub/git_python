# python scrapy框架 （github ArticleSpider）

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
                            
    2.scrapy 中 spider 的信号量
        (1) 
            ## 用于 scrapy 的信号
            from scrapy.xlib.pydispatch import dispatcher # 分发器
            from scrapy import signals      
            
        (2) 在 jobbole.py 中
                class JobboleSpider(scrapy.Spider):
                        # 使用selenium:
                             def __init__(self):
                                 dispatcher.connect(self.spider_closed, signals.spider_closed)
                            
                             def spider_closed(self, spider):
                                 # 当爬虫退出的时候 do_something
  
                                
```

## selector 类

```shell
    1.from scrapy.selector import Selector
    2.scrapy 中的 spider 类也是继承于 selector 类，其中 selector 类具有 xpath, css 方法
        # 对象的初始化，传入参数 text 为 html 格式的内容   
        selector = Selector(text=re.text)
        
        """
        在 id 为 ip_list 的节点下的 tr 节点
        <table id="ip_list">
          <tr class="odd">
            <td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn"></td>
            <td>122.237.104.62</td>
            <td>80</td>
            <td>浙江绍兴</td>
            <td class="country">高匿</td>
            <td>HTTPS</td>
              <td>2小时</td>
            <td>7分钟前</td>
          </tr>
        """
        all_trs = selector.css("#ip_list tr")
        """
            tr 也是一个 selector 选择器
        """
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            all_texts = tr.css("td::text").extract()
            ip = all_texts[0]
            port = all_texts[1]
            protocol = all_texts[5]
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
                先向 西刺免费代理IP 网站进行爬取 高匿IP 的信息, 存入到数据库中, 在 
                tools/crawl_cixi_ip.py 中定义随机获取 ip 代理的类 class GetIP(object)
        第二步:
                在 /ArticleSpder/middleware.py 中 定义 class RandomProxyMiddleware(object)
                进行 Scrapy 中 ip 代理的设置
                
    4. github 上 scrapy_proxies 项目有关于 ip 代理 相关处理
    5. github scrapy-crawlera 
            让我们 动态ip代理更加简单，不过要收费
         
    6. tor 
            洋葱浏览器，通过洋葱网络可以将本机 ip 进行匿名，
        
```

## 验证码识别

```shell
    1.编码实现(tesseract-ocr)
        tesseract-ocr 这是 google 开源的一个工具，最早是通过图片用来识别文字的，tesseract-ocr 识别率很低，
        不建议自己实现验证码的编码，开发效率低
    2.在线打码(推荐使用)
        识别率达到 90% 以上，识别速度较快，依靠的识别技术，主要是通过平台给我们的 api ，自己去调用
        在线打码平台：云打码，其中该平台要有 2 个账号,一个是开发者账号是用来测试的，另外一个则是用户账号
                    用来付钱的 
    3.人工打码
        保证任何复杂度验证码的识别，是人在识别你图片的验证码， 超速打码 项目
```

## settings.py 配置

```shell
    1.cookies 的禁用
        在 settings.py 文件中有
            # Disable cookies (enabled by default)
             COOKIES_ENABLED = False
            
            有的网站通过 cookies 来判断是否为爬虫，但是对于知乎等一些网站，如果将 cookies 禁用将登陆不成功。
            
    2.设置下载速度
        在 settings.py 文件中有
            DOWNLOAD_DELAY = 3 # 代表向网站请求下载的延迟，3秒钟请求下载一次
            
            AUTOTHROTTLE_ENABLED = True  # 开启自动限流功能
            AUTOTHROTTLE_START_DELAY = 5 # The initial download delay
            # The maximum download delay to be set in case of high latencies
            AUTOTHROTTLE_MAX_DELAY = 60
            AUTOTHROTTLE_DEBUG = False # 将延迟信息打印出来
            
    3.在不同的 Spider 中配置不同的 setting 值
           例如在同一个项目中需要不同的配置，知乎是需要 cookies 的参数的，而伯乐在线时不需要 cookies 的，
           但是一个项目只有 settings.py 一个文件。
           
           site-packages\scrapy\spiders\__init__.py 文件
                class Spider(object_ref):
                    name = None
                    custom_settings = None # 这个就是跟 settings.py 有关
                    
           所以在每一个不同的 spider 可以定义不同的 custom_settings，例如知乎
           zhihu.py
                class ZhihuSpider(scrapy.Spider):
                        # 通过对 custom_settings 的设置，可以覆盖掉 settings.py 默认的配置
                        custom_settings = {
                            "COOKIES_ENABLED":True
                        }
        
        
```

## Selenium(浏览器自动化测试框架 Selenium_spider.py)

```shell
    1.简介
        (1)
          Selenium 是直接运行在浏览器中，即 Selenium 是操控浏览器的，Selenium 是通过 driver 来控制浏览器，
          不同的浏览器对应的 driver 是不一样的
          
        (2) 作用
           有些网页是有 js 代码，浏览器通过渲染才有完整的 html 页面，而我们通过 Requests 模块下载的 html 则是
           不包含 js 代码的，所有数据会有缺失，我们可以通过 Selenium 来操作浏览器生成完整的 html 页面在进行下载.
           例如，我们在淘宝上想要拿到商品的价格(通过 js 代码加载的)，通过 Selenium 就可以获得
        
    2.安装 Selenium 
        (article_spider) > pip install selenium
        
    3.文档
        搜索 selenium python api (http://selenium-python.readthedocs.io/api.html)
        
    4.
        (1) 可以通过 Selenium 进行简单网页的爬取
                # 天猫价格获取
                browser.get("url")
                t_selector = Selector(text=browser.page_source)
                print(t_selector.css(".tm-promo-price .tm-price::text").extract())
                browser.quit()
                
        (2) 知乎模拟登陆
            """
                1.模拟浏览器找到 "登录" 按钮点击
                2.找到输入用户名的元素 进行输入 (send_keys)
                3.找到输入密码的元素 进行输入 (send_keys)
                4.找到 "登录" 按钮进行 点击(click)
            """
            browser.get("https://www.zhihu.com/signup?next=%2F")
            browser.find_element_by_css_selector(".SignContainer-switch span").click()
            browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input[name='username']").send_keys("18092671458")
            browser.find_element_by_css_selector(".SignFlow-password .SignFlowInput .Input-wrapper input[name='password']").send_keys("ty158917")
            browser.find_element_by_css_selector(".Button.SignFlow-submitButton.Button--primary.Button--blue").click()
        
        (3) 微博的模拟登录
                A. 微博开发平台
                B. # selenium 完成微博模拟登录
                    browser.get("http://weibo.com/")
                    """
                     这里要进行 sleep 是因为网页中 js 代码还没完全加载完，就开始 find_element_by_css_selector
                     这样有些元素是找不到的
                    """
                    import time
                    time.sleep(5)
                    browser.find_element_by_css_selector("#loginname").send_keys("1147727180@qq.com")
                    browser.find_element_by_css_selector(".info_list.password input[node-type='password'] ").send_keys("ty409760")
                    browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
                    
        (4) 模拟鼠标的滚动 (selenium执行JavaScript)
                当鼠标下拉到最下面时，会自动加载更多的内容，当获取页面是动态加载的情况，鼠标下滚非常有用
                # 开源中国博客:selenium执行JavaScript
                browser.get("https://www.oschina.net/blog")
                import time
                time.sleep(5)
                for i in range(3):
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
                    time.sleep(3)
                    
        (5) 设置chromedriver 不加载图片
                A. 作用
                    如果爬虫不加载图片，可以减少不必要的请求
                    
                B.
                    chrome_opt = webdriver.ChromeOptions()
                    prefs = {"profile.managed_default_content_settings.images":2}
                    chrome_opt.add_experimental_option("prefs", prefs)
                    browser = webdriver.Chrome(executable_path="./chromedriver.exe",chrome_options=chrome_opt)
                    browser.get("https://www.oschina.net/blog")
                    
        (6) phantomjs 的使用 (不推荐)
                无界面的浏览器， 多进程情况下phantomjs性能会下降很严重
                在我们的服务器系统中，例如 Centos, Linux，没有可视化的环境就可以使用 phantomjs
                
                browser = webdriver.PhantomJS(
                    executable_path="C:/spiderDriver/phantomjs-2.1.1-windows/bin/phantomjs.exe")
                browser.get("url")
                t_selector = Selector(text=browser.page_source)
                print (t_selector.css(".tm-price::text").extract())
                # print (browser.page_source)
                browser.quit()
                
        (7) 将 Selenium 集成到 scrapy 中
                可以在 ArticleSpider\ArticleSpider\middlewares.py 中进行编码
                第一步:
                    class JSPageMiddleware(object):
                            # 这样可以使得不打开很多浏览器
                            def __init__(self):
                                self.browser = webdriver.Chrome(
                                    executable_path="C:/spiderDriver/chromedriver.exe")
                                super(JSPageMiddleware, self).__init__()
                        
                            # 通过chrome请求动态网页
                            def process_request(self, request, spider):
                                if spider.name == "jobbole":
                                    self.browser.get(request.url)
                                    import time
                                    time.sleep(3)
                                    print ("访问:{0}".format(request.url))
                        
                                    """
                                        通过 Selenium 已经向网站请求页面
                                        了，就不需要再通过下载器进行二次下载了
                                        scrapy 一旦遇到 HtmlResponse，就不会用下载器
                                        下载页面，而是直接返回
                                    """
                                    return HtmlResponse(
                                        url=self.browser.current_url,
                                        body=self.browser.page_source,
                                        encoding="utf-8",
                                        request=request)
                                        
                第二步:
                    在 settings.py 中设置
                    DOWNLOADER_MIDDLEWARES = {
                        'ArticleSpider.middlewares.JSPageMiddleware': 643,
                        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                    }
                    
                以上有一个缺点是，当 jobbole 的 spider 运行完后，chrome页面是不会关闭的，因为没有调用
                 self.browser.quit()
                 解决方法
                    在 jobbole.py 中定义
                        class JobboleSpider(scrapy.Spider):
                                  # 使用selenium:
                                     def __init__(self):
                                         self.browser = webdriver.Chrome(executable_path="C:/spiderDriver/chromedriver.exe")
                                         super(JobboleSpider, self).__init__()
                                         # 当匹配到spider_closed这个信号时。关闭浏览器
                                         dispatcher.connect(self.spider_closed, signals.spider_closed)
                                    
                                     def spider_closed(self, spider):
                                         # 当爬虫退出的时候关闭chrome
                                         print("spider closed")
                                         self.browser.quit()
                                         
                    在 ArticleSpider\ArticleSpider\middlewares.py 中
                        class JSPageMiddleware(object):                            
                                # 通过chrome请求动态网页
                                def process_request(self, request, spider):
                                    if spider.name == "jobbole":
                                        spider.browser.get(request.url)
                                        import time
                                        time.sleep(3)
                                        print ("访问:{0}".format(request.url))
                            
                                        """
                                            通过 Selenium 已经向网站请求页面
                                            了，就不需要再通过下载器进行二次下载了
                                            scrapy 一旦遇到 HtmlResponse，就不会用下载器
                                            下载页面，而是直接返回
                                        """
                                        return HtmlResponse(
                                            url=spider.browser.current_url,
                                            body=spider.browser.page_source,
                                            encoding="utf-8",
                                            request=request)      
                                            
        (8) 在无界面的情况下运行 chrome (在 Centos 等linux 环境)
                 (A) 安装 pyvirtualdisplay
                        (article_spider) λ pip install pyvirtualdisplay\
                        
                 (B)                         
                        from pyvirtualdisplay import Display
                        # 界面不可见
                        display = Display(visible=0, size=(800,600))
                        display.start()
                        browser = webdriver.Chrome()
                        browser.get(url)
                        
                        错误排查:
                            原因: easyprocess.EasyProcessCheckInstalledError: cmd=['Xvfb', '-help'] OSError=[Errno 2] 
                            No such file or directory
                                > sudo apt-get install xvfb
                                > pip install xvfbwrapper
        (9) 关于爬取动态页面
                解决方案:
                    A. selenium chrome driver (优先使用)
                    B. scrapy splash (支持分布式)
                    C. selenium grid (支持分布式)
                    
        (10) 工具介绍
                (A) github splinter
                        让我们可以操控浏览器的解决方案
                            
    * 注意
           A. 在获取含有 js 代码的页面时要考虑到 js 代码渲染到浏览器的时间， 不能通过 Selenium get方法之后，马上
              find_element_by_css_selector，要等待几秒
       
```

## scrapy 的暂停和开启

```shell
    1.我们可以实现在 scrapy 爬取的过程中进行暂停，同时保存爬取的进度，下次开始时继续从停止
      开始，而不是重新开始
      
    2.
        D:\python_example\ArticleSpider (master -> origin)
        (article_spider) λ scrapy crawl  lagou -s JOBDIR=job_info/001
            其中 scrapy 暂停需要保存一些数据， 
            -s : set
            JOBDIR 为 保存数据的文件夹
                job_info 为文件夹，001 也是文件夹，不同的 spider 是不能共用同一文件夹的，而且相同的
                spider 如果想要重新爬取则 001 要变为 002
                
            scrapy 爬虫的结束信号是用 ctrl + C 来实现的， 而用 pycharm IDE 则无法模拟暂停
            
    3.操作步骤
        步骤一:
            (article_spider) λ scrapy crawl  lagou -s JOBDIR=job_info/001
            
        步骤二:
            执行一次 ctrl + C ，进行暂停
            
        步骤三:
             (article_spider) λ scrapy crawl  lagou -s JOBDIR=job_info/001
             继续执行
```

## scrapy 去重原理

```shell
    1.去重的中间件
        site-packages\scrapy\dupefilters.py
            class RFPDupeFilter(BaseDupeFilter) 去重器，是 scrapy 中默认的去重器
            RFPDupeFilter 类里有个方法 request_seen ， 这个是由 site-packages\scrapy\core\scheduler.py
            中的 
                class Scheduler(object): 
                        def enqueue_request(self, request):
                        if not request.dont_filter and self.df.request_seen(request): # 队列中已经有相同的url
                        
            request_seen 方法其实是对 request 进行转化为 固定的 hash 值，再跟看看是否在 set() 集合中，来达到去重效果
                            
```

## scrapy telnet 

```shell
    1.当 scrapy crawl lagou 后，在终端会打印该服务会开启 telnet 服务
    2.> telnet ip port (连接到 telnet 服务器上)
          >>> est() # 查看 scrapy 服务的状态信息
          >>> settings["COOKIES_ENABLED"]
          结果:
               False
          
    3.相关文档
        https://doc.scrapy.org/en/latest/topics/telnetconsole.html
        
    4.源码
        在 scrapy 的扩展中 \site-packages\scrapy\extensions\telnet.py
```

## scrapy 数据收集

```shell
    1.有的插件会对状态进行收集，文档查看 Stats Collection 
    2.spider 在运行的时候有一个数值进行计数 request 的个数，以及 spider 中的 parse 函数到底
      yield 多少个 item, self.crawler.stats 对象一般不会保存 list
      
    3. 源码:
            site-packages\scrapy\statscollectors.py
            用的最多的是 class MemoryStatsCollector(StatsCollector)
            
    4.使用数据收集器
        Spider 中统计 404页面的个数以及 url
        class JobboleSpider(scrapy.Spider):
                # 收集伯乐在线所有404的url以及404页面数
                """
                    handle_httpstatus_list 默认是不包含 404，
                    需要对 404 的页面进行处理，则需要将 404 加入到handle_httpstatus_list中
                """
                handle_httpstatus_list = [404]
            
                """
                    我们要收集404的url以及404页面数
                    则必须要 self.fail_urls 进行保存
                """
                def __init__(self):
                    self.fail_urls = []
                    dispatcher.connect(self.handle_spider_cosed, signals.spider_closed)
            
                def handle_spider_cosed(self, spider, reason):
                    self.crawler.stats.set_value("failed_urls", ",".join(self.fail_urls))
                    pass
                    
                def parse(self, response):
                    # 如果状态值为404
                    if response.status == 404:
                        self.fail_urls.append(response.url)
                        self.crawler.stats.inc_value("failed_url")
        
```

## scrapy 信号(很重要)

```shell
    1.Scrapy使用信号来通知事情发生。可以在Scrapy项目中捕捉一些信号(使用 extension)来完成额外的工作或添加额外的功能，
      扩展Scrapy。我们的 MiddleWare 实际上也是 extension 中的一种，只是 MiddleWare 中只处理某些信号。
      
    2.内置信号
        engine_started : 当Scrapy引擎启动爬取时发送该信号
        engine_stopped : 当Scrapy引擎停止时发送该信号(例如，爬取结束)
        spider_closed:  当某个spider被关闭时，该信号被发送。
                        该信号可以用来释放每个spider在 spider_opened 时占用的资源。
        spider_opened : 当spider开始爬取时发送该信号。该信号一般用来分配spider的资源，不过其也能做任何事。
                        比如我们要记录 spider 开始爬取的时间，则可以捕捉该信号，回调函数中可以将开始时间放到
                        数据收集器中
                        
        spider_idle： 当spider进入空闲(idle)状态时该信号被发送。
                      空闲意味着:
                        requests正在等待被下载
                        requests被调度
                        items正在item pipeline中被处理
                        
    3.使用
        对 spider_closed 信号进行处理
        在 jobbole.py 中
        class JobboleSpider(scrapy.Spider):
                def __init__(self):
                    # 对 signals.spider_closed 信号进行注册
                    dispatcher.connect(self.handle_spider_cosed, signals.spider_closed)
            
                #  其中 handle_spider_cosed 函数的参数是由 signals.spider_closed 信号决定的
                def handle_spider_cosed(self, spider, reason):
                    pass
         
```

## scrapy 扩展

```shell
    1.中间件实际上只能重载几个函数，例如 
            Downloader Middleware 中间件
              process_request(request, spider)，
              process_response(request, response, spider)，
              process_exception(request, exception, spider) 三个函数
              
    2.中间件都是缩减版的扩展，每个扩展是一个单一的Python class. Scrapy扩展(包括middlewares和pipelines)的主要入口是 
      from_crawler 类方法， 它接收一个 Crawler 类的实例.通过这个对象访问settings，signals，stats，
      控制爬虫的行为。
      通常来说，扩展关联到 signals 并执行它们触发的任务
      
    3.自定义扩展需要自己绑定 signal 处理函数
    4. 例子
        import logging
        from scrapy import signals
        from scrapy.exceptions import NotConfigured
        
        logger = logging.getLogger(__name__)
        
        class SpiderOpenCloseLogging(object):
        
            def __init__(self, item_count):
                self.item_count = item_count
        
                self.items_scraped = 0
        
            @classmethod
            def from_crawler(cls, crawler):
                # first check if the extension should be enabled and raise
                # NotConfigured otherwise，从settings.py 配置中读取 MYEXT_ENABLED 是否为 True
                if not crawler.settings.getbool('MYEXT_ENABLED'):
                    raise NotConfigured
                # get the number of items from settings
        
                item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)
        
                # instantiate the extension object
        
                ext = cls(item_count)
        
                # connect the extension object to signals, 将信号绑定对应的处理函数
        
                crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        
                crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        
                crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        
                # return the extension object
        
                return ext
        
            def spider_opened(self, spider):
                logger.info("opened spider %s", spider.name)
        
            def spider_closed(self, spider):
                logger.info("closed spider %s", spider.name)
        
            def item_scraped(self, item, spider):
                self.items_scraped += 1
                if self.items_scraped % self.item_count == 0:
                    logger.info("scraped %d items", self.items_scraped)
                    
    5.源码分析
        site-packages\scrapy\extensions\corestats.py
        class CoreStats(object) 类主要是用来实现收集 scrapy 相关信息，例如
            class CoreStats(object):
                def __init__(self, stats):
                    self.stats = stats
            
                @classmethod
                def from_crawler(cls, crawler):
                    o = cls(crawler.stats)
                     # spider_opened 信号来时 调用 spider_opened 记录开始时间
                    crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
                    crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
                    crawler.signals.connect(o.item_scraped, signal=signals.item_scraped)
                    crawler.signals.connect(o.item_dropped, signal=signals.item_dropped)
                    crawler.signals.connect(o.response_received, signal=signals.response_received)
                    return o
            
                def spider_opened(self, spider):
                    self.stats.set_value('start_time', datetime.datetime.utcnow(), spider=spider)
            
                def spider_closed(self, spider, reason):
                    self.stats.set_value('finish_time', datetime.datetime.utcnow(), spider=spider)
                    self.stats.set_value('finish_reason', reason, spider=spider)
            
                def item_scraped(self, item, spider):
                    self.stats.inc_value('item_scraped_count', spider=spider)
            
                def response_received(self, spider):
                    self.stats.inc_value('response_received_count', spider=spider)
            
                def item_dropped(self, item, spider, exception):
                    reason = exception.__class__.__name__
                    self.stats.inc_value('item_dropped_count', spider=spider)
                    self.stats.inc_value('item_dropped_reasons_count/%s' % reason, spider=spider)
```