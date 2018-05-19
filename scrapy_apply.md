# scrapy 应用
 
## scrapy结构目录

```shell

    1.ArticleSpider/pipelines.py: 数据存储相关的地方
    2.ArticleSpider/middlewares.py : 定义自己middlewares让spider更加可控
    3.spiders目录则存放的是具体某个网站的爬虫

```

## 相关知识

```shell
    1.要对某个url进行调试，在运行后这个命令后已经获取url的内容，这样接下来就可以在cmd进行相关的调试
        (article_spider)项目路径> scrapy shell http://blog.jobbole.com/110287/
            (1) >>> title = response.xpath('//div[@class="entry-header"]/h1/text()');
                >>> title
                    结果：
                    [<Selector xpath='//div[@class="entry-header"]/h1/text()' data='2016 腾讯软件开发面试题（部分）'>]
                >>> title.extract()
                    ['2016 腾讯软件开发面试题（部分）']
                >>> title.extract()[0]
                    '2016 腾讯软件开发面试题（部分）'
```

## css 选择器

```shell
    1.表达式
        (1) *
            选择所有节点
            
        (2) #container
            选择id为container的节点
            
        (3) .container
            选取所有class包含的cont ainer的节点
            
        (4) li a
            选取所有li下的所有a节点
          
        (5) ul + p
            选取ul后面的第一个元素
            
        (6) div#container > ul
            选取id为container的div的第一个ul子元素
            
        (7) ul ~ p
            选取与ul相邻的所有p元素
            
        (8) a[title]
            选取所有有title属性的a元素
            
        (9) a[href="http://jobbol.com"]
            选取所有href属性为jobbole.com值的a元素
            
        (10) a[href*="jobole"]
            选取所有href属性包含jobbole的a元素
            
        (11) a[href^="http"]
            选取所有href属性值以"http"开头的a元素
            
        (12) a[href$=".jpg"]
            选取所有href属性值以".jpg"结尾的a元素
            
        (13) input
```