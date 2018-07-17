# python scrapy框架
 
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

