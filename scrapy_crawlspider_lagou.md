# scrapy 拉勾网应用

## 安装环境

```shell
    1.(article_spider) D:\Program Files\PowerCmd> pip install requests
```

## 注意事项

```shell

```

## crawlSpider 

```shell
    1.crawlSpider 将我们整个 spider 进行进一步的包装, 其中 最重要的是 rules 类, 我们只需要定义好
      rules 的规则, 则 crawlSpider 会根据规则进行爬取
      
    2.源码分析
        class CrawlSpider(Spider): 可以看出 CrawlSpider 是继承 Spider,
        而 class Spider 有一个函数是
        
            def start_requests(self):
                cls = self.__class__
                if method_is_overridden(cls, Spider, 'make_requests_from_url'):
                    warnings.warn(
                        "Spider.make_requests_from_url method is deprecated; it "
                        "won't be called in future Scrapy releases. Please "
                        "override Spider.start_requests method instead (see %s.%s)." % (
                            cls.__module__, cls.__name__
                        ),
                    )
                    for url in self.start_urls:
                        yield self.make_requests_from_url(url)
                else:
                    for url in self.start_urls:
                        yield Request(url, dont_filter=True)
                        
            这个 start_requests 会去遍历我们的 start_urls.
            
        既然 CrawlSpider 继承 Spider, 则它的入口也是从 start_requests 开始,同时 start_requests 函数中
        默认callback 是 parse,而 CrawlSpider 类中已经重载 parse 函数:
             def parse(self, response):
                    # self._parse_response 函数是非常重要的
                    return self._parse_response(response, self.parse_start_url, cb_kwargs={}, follow=True)
                    
                    
             """
                _parse_response 这个函数是 CrawlSpider的核心函数
             """       
             def _parse_response(self, response, callback, cb_kwargs, follow=True):
                   """
                        首先判断是否有 callback, 而在 parse 中 callback = self.parse_start_url
                        而 self.parse_start_url 这个函数我们可以进行重载,可以加入自己的逻辑,
                        如果我们不重载 parse_start_url函数, 和 process_results 函数, 则
                        if callback 语句块中不会实现任何东西
                   """   
                if callback:
                    ## 相当于自己调用了 parse_start_url(response, cb_kwargs)   
                    cb_res = callback(response, **cb_kwargs) or ()
                    
                    #  def process_results(self, response, results):
                    #          return results
                    #  实际上返回的是 callback 的返回值
                    cb_res = self.process_results(response, cb_res)
                    for requests_or_item in iterate_spider_output(cb_res):
                        yield requests_or_item
        
                   """
                        下面的 for 循环操作,则是 CrawlSpider 中的核心的核心
                        if follow and self._follow_links 主要是判断 CrawlSpider 是不是应该
                        follow, self._follow_links 的值则可以在 setting 中进行设置
                   """   
                if follow and self._follow_links:
                    for request_or_item in self._requests_to_follow(response):
                        yield request_or_item
                        
           """
                
           """              
            def _requests_to_follow(self, response):
                # 首先判断 response 是不是符合 HtmlResponse
                if not isinstance(response, HtmlResponse):
                    return
                # 主要是通过 seen 将 response 去重
                seen = set()
                for n, rule in enumerate(self._rules):
                    links = [lnk for lnk in rule.link_extractor.extract_links(response)
                             if lnk not in seen]
                    ## 自己抽取出来的 links, 在调用 自己定义的 rule.process_links
                    if links and rule.process_links:
                        links = rule.process_links(links)
                        
                    ## 抽取完 link 直接
                    ##   def _build_request(self, rule, link):
                    ##       r = Request(url=link.url, callback=self._response_downloaded)
                    ##       r.meta.update(rule=rule, link_text=link.text)
                    ##       return r
                    for link in links:
                        seen.add(link)
                        r = self._build_request(n, link)
                        yield rule.process_request(r)
                        
                其中 rule.link_extractor.extract_links(response) 是针对于 
                    class LagouSpider(CrawlSpider):
                            rules = (
                                        Rule(LinkExtractor(allow=r'Items/'), callback='parse_job', follow=True),
                                    )
                                    
                    实际上从 response 中 抽取出 对应的LinkExtractor对象
                    
        所以在应用层(lagou.py)不能够在 重载 parse函数了, 这跟 知乎,伯乐在线不一样.
        
    3. 
        class Rule(object):

            def __init__(self, link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=identity):
                self.link_extractor = link_extractor
                self.callback = callback
                self.cb_kwargs = cb_kwargs or {}
                self.process_links = process_links
                self.process_request = process_request
                if follow is None:
                    self.follow = False if callback else True
                else:
                    self.follow = follow
                    
            follow：代表满足 rule 中的 link, 要不要进一步的跟踪
            process_links : 可以对 rule 中的 link, 进行预处理
            
            
    4. LinkExtractor 类
                def __init__(self, allow=(), deny=(), allow_domains=(), deny_domains=(), restrict_xpaths=(),
                 tags=('a', 'area'), attrs=('href',), canonicalize=False,
                 unique=True, process_value=None, deny_extensions=None, restrict_css=(),
                 strip=True):
                        tags, attrs = set(arg_to_iter(tags)), set(arg_to_iter(attrs))
                        tag_func = lambda x: x in tags
                        attr_func = lambda x: x in attrs
                        lx = LxmlParserLinkExtractor(
                            tag=tag_func,
                            attr=attr_func,
                            unique=unique,
                            process=process_value,
                            strip=strip,
                            canonicalized=canonicalize
                        )
                        
                 其中 
                     allow() : 可以用于正则表达式, 例如 allow=r'www.lagou.com/jobs/', 其url来判断 是不是
                                符合 allow 的正则表达式,符合该 allow 就去提取
                                
                     deny() : 符合 deny 中 的 url 就抛弃不做
                     
                     allow_domains() : 例如 allowed_domains = ['www.lagou.com'], 这个 www.lagou.com
                                       域名下面的 url 就进行提取
                                       
                     restrict_xpaths() : 它可以进一步得去限定我们的 url, 通过 xpath 进一步得进行区域的限定

```


## 通过scrapy 的 crawlspider 模板进行爬虫

```shell
    1.进入到项目目录中
        D:\python_example\ArticleSpider\ArticleSpider>
        
    2.切换到虚拟环境中
        D:\python_example\ArticleSpider\ArticleSpider>workon article_spider
        结果：
        (article_spider) D:\python_example\ArticleSpider\ArticleSpider>
        
    3.生成一个爬虫模板
        (article_spider) D:\python_example\ArticleSpider\ArticleSpider> scrapy genspider -t crawl lagou www.lagou.com
        
        问题:
            (1) 出现 ImportError:No module named 'utils'
                    在 pycharm IDE 中 已经将项目 ArticleSpider 设置为 Source Root,
                    所以在 ArticleSpider 目录下 items.py 文件中 导入模块可以从
                    from ArticleSpider.utlils.common import extract_num 改变为
                    from utlils.common import extract_num.
                    在 pycharm IDE 里面是没有任何问题(Run->Edit Configurations中 以及将
                    Add Source Root to PYTHONPAHT )
                    但是在 cmd 中是不识别的,
                    解决方法:
                        在 settings.py 中 写入:
                            import os
                            import sys
                            """
                                sys.path.insert 函数主要是将某个路径插入到 pathonpath 中
                                第一个参数是序列号
                                第二个参数是要插入的路径名
                            """
                            project_dir = os.path.dirname(os.path.abspath(__file__))
                            sys.path.insert(0, project_dir)
```

## 调试过程

```shell
    1.D:\python_example\ArticleSpider (master -> origin)
      (article_spider) > scrapy shell https://www.lagou.com/jobs/3056076.html
      
      结果:
        2018-07-15 13:27:30 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.lagou.com/jobs/3056076.html> 
                                                        (referer: https://www.lagou.com/)
        [s] Available Scrapy objects:
        [s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
        [s]   crawler    <scrapy.crawler.Crawler object at 0x0370AE90>
        [s]   item       {}
        [s]   request    <GET https://www.lagou.com/jobs/3056076.html>
        [s]   response   <200 https://www.lagou.com/jobs/3056076.html>
        [s]   settings   <scrapy.settings.Settings object at 0x03E80FD0>
        [s]   spider     <LagouSpider 'lagou' at 0x51115f0>
        [s] Useful shortcuts:
        [s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
        [s]   fetch(req)                  Fetch a scrapy.Request and update local objects
        [s]   shelp()           Shell help (print this help)
        [s]   view(response)    View response in a browser
                                                        
      说明拉勾网并没有验证我们的 user_agent
      
    2.再进行 css,xpath 的提取
        >>> response.css(".job-name::attr(title)").extract()
        结果:
             ['web前端开发']
        
```

## 编码流程

```shell
    1.数据库设计
        首先要对爬取的网站进行分析, 确定要保存的数据, 对数据库的表结构进行设计
        
    2.在 item.py 设计 对应的 item
    3.在 对应的解析 parse函数 对 response 进行 css/xpath 解析, 这里可以用 itemLoader.css/itemLoader.xpath
      只进行区域得提取, 之后的解析处理可以放在 item.py 中定义的 item中处理

```

## 问题

```shell
    1.爬虫过于频繁
       DEBUG: Redirection (302) to <GET http://forbidden.lagou.com/forbidden/fb.html?ip=110.184.71.186> from
       <GET https:// https://www.lagou.com>
       
       这里你主机的ip 为 110.184.71.186
       
    2.通过按 F12 获取 html 的信息其实是浏览器通过 js动态加载后的效果图, 但是用 scrapy框架请求返回的 response是不一样的
      查询需要右键查看源码
```

