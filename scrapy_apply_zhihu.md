# scrapy 知乎应用

## 安装环境

```shell
    1.(article_spider) D:\Program Files\PowerCmd> pip install requests
```

## 注意事项

```shell
    (1) requests 模块用 get() 方法时, 传入参数中headers中user-agent字段的默认设置为python2或则python3,
            而不是浏览器的
                Mozilla/5.0 (Windows NT 6.1; Win64; x64) 
                AppleWebKit/537.36 (KHTML, like Gecko)
                Chrome/63.0.3239.108 
                Safari/537.36
            这样有些网站的服务器会检测user-agent字段合不合法，如果不合法,则会返回 状态码为500的错误
            
    (2) 使用requests模块模拟浏览器对知乎网站进行获取数据和发送数据时,传入的参数都要带有 headers
    (3) 如果是一次常连接,可以使用request模块中的session对象,而不用每次都是request.get()或则request.post()
            
            def zhihu_old_login(account, password):
                        post_url = "https://www.zhihu.com/login/phone_num"
                
                        # 需要向该post_url 传递的数据
                        post_data = {
                            "_xsrf":get_xsrf(),
                            "phone_num":account,
                            "password":password
                        }
                
                        # 模拟登录这里利用的requests模块的session
                        # 使用session进行post 方法,而不是每次都用requests.post()
                        response_text = session.post(post_url, data = post_data, headers=headers)
                        
        如果在 get_xsrf() 函数中用到 使用session进行get方法, 则 get_captcha() 获取登录的验证码一定要通过
        使用session进行get方法
                        
    (4) 传统的session对象 session.cookies.save() 的 cookies类是没有save()方法的,
        可以通过
            # 保证python2 和 python3 的兼容代码
            try:
                # python2 是 cookielib
                import cookielib
            except:
                # 出现异常则是python3 的环境,将http.cookiejar重命名为 cookielib
                import http.cookiejar as cookielib
                
            session.cookies = cookielib.LWPCookieJar(filename="cookies.txt") 来解决,其中参数filename自定义保存文件名
            
    (5) 当要将程序中的内容保存到文件中,其保存的编码格式为utf-8
    
             with open("index_page.html", "wb") as f:
                 f.write(response.text.encode("utf-8"))
                 
    (6) 如何判断状态为用户登录状态
            某些url一定是在用户登录状态下才能访问的,通过对url进行数据获取得到 response.statut_code 判断是不是为200，
            如果不是200,则为未登录状态
            
    (7) 当用requests模块或则session对象进行get()方法时,如果传入参数 allow_redirects 没有显式设置为
        False,则会重定向到新的url而且返回的状态码为200,这样不太符合业务, 我们需要知道要求的url返回的状态码
        而不是重定向后的状态码.
                session.get(inbox_url, headers=headers, allow_redirects=False)
                
    (8) 知乎的防爬机制： 同一个ip 或则 同一个 user_agent, request 请求频率过快
```

## scrapy 框架知识

```shell
    1.scrapy 框架默认是先从 def start_requests(self), 这个方法在 scrapy 类中 有默认的实现
                例如:
    
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
                            yield Request(url, dont_filter=True)  #其中这里没有定义 callback 方法,则默认为 parse 
                            
        所以我们如果要在请求页面前先进行 登录, 则可以重载 start_requests 方法, 现在 start_requests 方法中进行用户的登录,
        在进行 prase 的解析方法
        
    2.  def do_insert(self, cursor, item)   
            传入参数 item, 我们可以知道 它是哪个 class,例如:
                item.__class__.__name__ == "JobBoleArticleItem"
                
                
            def do_insert(self, cursor, item):
                    """
                        根据不同的 item 构建不同的 sql 语句并插入到 MySQL 中
                    """
            
                    if item.__class__.__name__ == "JobBoleArticleItem": # 这种硬编码的方式,在后续修改的时候比较麻烦
                        #执行具体得插入
                        insert_sql = "xxx"
                        cursor.execute(insert_sql, XXXXX)
                        
    3.在 settings.py 定义了参数,例如:
            SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            SQL_DATE_FORMAT = "%Y-%m-%d"
            
       需要在其他文件进行引用,则需要 
            from ArticleSpider.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT
            
       这样就可以继续引用了
       
    4.错误解析
       (1) MySQL 中 出现 "Unknown column 'comments_nums' in 'field list'" , 
           说明该 comments_nums 列在数据库表结构中不存在
            
       (2) "Duplicate entry "xxx" for key 1
            说明 插入重复数据导致主键冲突
        
    5.在 debug 进行 yield 异步调试时
          可以先修改代码 以使它能够同步调试, 例如 在循环的 yield 语句中 加入 break 等等;
    6.
        """
            当数据库中出现插入冲突(主键相同),使用 MySQL 特有的语句 使得
            主键不动, 只更新指定的字段
        """
        insert_sql = """
                               insert into zhihu_answer(zhihu_id, url, 
                               question_id, author_id, content, praise_num, 
                               comments_num, create_time, update_time,
                               crawl_time) 
                               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                               ON DUPLICATE KEY UPDATE content=values(content),
                               comments_num=values(comments_num), praise_num=values(praise_num),
                               update_time=values(update_time);
                      """
                      这里如果插入一条数据,其主键 zhihu_id 已经存在, 则对已存在的记录 只更新 content，
                      comments_num, praise_num, update_time 等字段
                      
    7.在 scrapy 中 登录(login_url)的时候需要验证码(captcha_url), 一定要确保 请求这 2个url的 cookies 一致,
      详细内容参照知乎登录代码, 提示 在 scrapy.Request(login_url)时, 在 response 返回函数中 重新 yield 
      scrapy.Request(captcha_url)
                      
```

## 知乎业务

```shell
    1.使用 scrapy 框架进行深度优先爬虫顺序
            先进入 def start_requests(self), 再进入  def login(self, response), 再进入  def check_login(self, response)
            再进入 默认的方法 parse(), 在 parse 中处理 response 返回中页面, 提取出该页面的所有 url, 再从中提取出 关于
            question 的 url(https://www.zhihu.com/question/20702054), 再向 每个 question 的 url 进行请求
            
            yield scrapy.Request(request_url, headers=headers, callback=self.parse_question), 收到响应的
            response再 在 parse_question中进行 question 相关的解析, 解析完后 yield question_item 交给 pipeline.py
            进行数据库相关操作, 同时每一个 question 解析中, 向 answer 请求 
            yield scrapy.Request(self.start_answer_url.format(question_id, 5, 0),
                             headers=headers,
                             callback=self.parse_answer)
                             
            其中初始的answer_url 是 在google浏览器中按F12进行网络调试,按下知乎中的 "查看更多的按钮", 
            在network中查看相应的url
            例如https://www.zhihu.com/api/v4/questions/20899988/answers?
                include=.....offset=13&limit=5&sort_by=default

            

```
 
## 知乎的登录流程

```shell

    1.登录时了解到是向哪个url进行post, 以及post 的内容是什么
    2.在google浏览器中按F12进行网络调试,按下知乎中的 "查看更多的按钮", 在network中查看相应的url
      例如https://www.zhihu.com/api/v4/questions/20899988/answers?
                include=.....offset=13&limit=5&sort_by=default
      再将该url输入到浏览器中,通过jsonviewer插件进行json格式化
      可以看到如下内容
        {
            data: [.....],
            paging: {
                    is_end: false,
                    is_start: false,
                    next: "https://www.zhihu.com/api/v4/questions/20899988/answers?include=.....limit=5&offset=18&sort_by=default",
                    previous: "https://www.zhihu.com/api/v4/questions/20899988/answers?include=....limit=5&offset=8&sort_by=default",
                    totals: 223  //回答数总共是 223个
                    }
        }
        
        注意:
            在paging中总共的回答数是223,当前的页面的回答数是5(limit=5),offset从13~17, 而下一页面是从offset=18开始
            而 is_end 则表示当前 url 是不是最后的, 如果 is_end 值为 true,则 next 的 url 则没有必要再取.
            
            在data中保存有
                id: 24923424,
                type: "answer",
                question: {...},
                author: {...},  ## author 中 id 可能不存在,因为用户会匿名回答
                url: "https://www.zhihu.com/api/v4/answers/24923424",
                created_time: 1398451573,
                updated_time: 1400431225,
                voteup_count: 12612,
                comment_count: 283,
                content:回答的内容
                
    3.对于知乎的爬取则采用深度优先算法
    4. 知乎登录时请求验证码的 url: "https://www.zhihu.com/captcha.gif?r=时间戳*1000&type=login
                               https://www.zhihu.com/captcha.gif?r=1531232894046&type=login

```

## 数据库设计

```shell
    1. zhihu_question
        字段                  数据类型          解释
        zhihu_id             bigint    
        topics               varchar(255)
        url                  varchar(300)
        title                varchar(200)
        content              longtext        问题的内容,不知道内容的大小所以只能定 longtext
        create_time          datetime        问题的创建时间
        update_time          datetime        问题的更新时间
        answer_num           int
        comments_num         int
        watch_user_num       int             关注者数量
        click_num            int             被浏览数量
        crawl_time           datetime        最新的爬取时间戳
        crawl_update_time    datetime        最新的内容被更改
    
    2. zhihu_answer
          字段                  数据类型          解释
        zhihu_id             bigint    
        url                  varchar(300)
        question_id          bigint
        author_id            varchar
        content              longtext        问题的内容,不知道内容的大小所以只能定 longtext
        praise_num           int
        comments_num         int
        create_time          date            问题的创建时间
        update_time          date            问题的更新时间
        crawl_time           datetime        最新的爬取时间戳
        crawl_update_time    datetime        最新的内容被更改
```

## 通过scrapy 来模拟登录 知乎

```shell
    1.进入到项目目录中
        D:\python_example\ArticleSpider\ArticleSpider>
        
    2.切换到虚拟环境中
        D:\python_example\ArticleSpider\ArticleSpider>workon article_spider
        结果：
        (article_spider) D:\python_example\ArticleSpider\ArticleSpider>
        
    3.生成一个爬虫模板
        (article_spider) D:\python_example\ArticleSpider\ArticleSpider> scrapy genspider zhihu www.zhihu.com
        注意:
            genspider 没有指明特定的模板时, 默认的是使用 basic 模板
```

## 知乎调试信息

```shell
         在 scrapy shell 中,向url请求数据时,默认的headers中user_agent为python2,如果想要以浏览器的身份去请求,
                (article_spider) D:\python_example\ArticleSpider\ArticleSpider>  scrapy shell -s
                 USER_AGENT="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
                 Chrome/63.0.3239.108 Safari/537.36"  https://www.zhihu.com/question/281967318
```

