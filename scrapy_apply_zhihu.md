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
```

## 知乎业务

```shell
    

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
                
    3.对于知乎的爬取则采用深度优先算法,

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
```

