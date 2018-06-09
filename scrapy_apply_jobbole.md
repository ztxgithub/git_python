# scrapy 应用
 
## scrapy结构目录

```shell

    1.ArticleSpider/pipelines.py: 数据存储相关的地方
    2.ArticleSpider/middlewares.py : 定义自己middlewares让spider更加可控
    3.spiders目录则存放的是具体某个网站的爬虫

```

## scrapy 程序运行流程
```shell
    1.先在项目的spiders目录下jobbole.py进行运行(如果有用到itemLoader,则会到items.py文件中运行预处理函数)
    2.再到自定义的pipeline.py中进行运行,运行的顺序根据settings.py中的设置的参数有关
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
                    
    2. extract_first() (只对scrapy的response.css或则response.xpath返回值有效)
           取数组的第一个元素,当该数据为NULL时可以传递默认参数
                comment_text_css = response.css("a[href='#article-comment'] span::text").extract_first()
                这样是为了防止 response.css("a[href='#article-comment'] span::text").extract()[0] 
                数组为内容为空，取第一个元素抛异常
                
     
    3.在提取某些网站时，有的时候是相对于当前域名(http://blog.jobbole.com)的 相对路径例如：114009/,
      实际上是指向http://blog.jobbole.com/114009/, 所以要 response.url + post_url(相对路径)
      调用urllib模块
      from urllib import parse
      parse.urljoin(response.url,post_url)
```

## css 选择器

```shell
    1.表达式
        (1) *
            选择所有节点
            
        (2) #container
            选择id为container的节点
            
        (3) .container
            选取所有class包含的其class="container"的节点
            (可以是class="container",也可以是 class="123 container 345")
            <div class="entry-header"> 对应于 response.css(".entry-header")
            
            
        (4) li a
            选取所有li节点下的所有a节点
          <div class="entry-header">
	            <h1>2016 腾讯软件开发面试题（部分）</h1>
		  </div>
		  选取该class下的h1节点
		    response.css(".entry-header h1")
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
            
        (13) input[type=radio]:checked
            选择选中的radio的元素
            
        (14) div:not(#container)
            选取所有id非container的div属性
            
        (15) li:nth-child(3)
            选取第三个li元素
            
        (16) tr:nth-child(2n)
            第偶数个tr
            
    2.获取某个节点下的内容
        >>> response.css(".entry-header h1::text").extract()
            ['2016 腾讯软件开发面试题（部分）']
            
        通过class="entry-meta-hide-on-mobile"找到对应的p节点取其内容
        >>> response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip()
        '2017/02/18 ·'
        
    3.通过css选择某个节点的中某个属性值
        获取class值为post-thumb节点下面的a节点的href的值
        <div class="post-thumb">
            <a href="http://blog.jobbole.com/114009/" >
		</div>
		
		>>> response.css(".post-thumb a::attr(href)")
		
    4.如果一个节点的class同时包含多个值
        <a class="next page-numbers" href="http://blog.jobbole.com/all-posts/page/2/">下一页 »</a>
        选出该节点,class值同时有next和page-numbers
        
        >>> response.css(".next.page-numbers")
```

## scrapy中spiders目录下parse

```shell
    1.其中response.css()或则response.xpath()返回的是 selector对象
      而 selector对象还可以 selector.css()进行递归提取
      例如:
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            
    2.  在第一层提取相关的url，通过yield Request可以向下传递参数进行函数处理
        其中第一个参数url是给回调函数self.parse_detail用的，在parse_detail函数中的response.css()或则
        response.css()是针对url=parse.urljoin(response.url,post_url)这个url的，如果想再向
        回调函数self.parse_detail传递一些参数,则使用第二个参数 meta
        yield Request(url=parse.urljoin(response.url,post_url),
                      meta={"front_image_url":image_url}, 
                      callback=self.parse_detail)
```

## pipelines.py

```shell
    1.如果要使pipe-+
    lines.py生效，则在settings.py中去注释
            ITEM_PIPELINES = {
                                 'ArticleSpider.pipelines.ArticlespiderPipeline': 300,
                              }
                              
    2.items.py与pipelines.py连用,在spiders/jobbole.py中回调函数 yield article_item(Items),会直接跳转到
      pipelines.py中的 process_item函数,pipelines.py主要用作数据存储
```

## scrapy 做到图片的下载

```shell
    1.在settings.py
        ITEM_PIPELINES = {
                           'ArticleSpider.pipelines.ArticlespiderPipeline': 300,
                           'scrapy.pipelines.images.ImagesPipeline':1   # 数值越小，越先调该函数,是等spiders目录下parse调好
                                                                        # 再掉 pipeline
                         }
                       
        # 从哪里去下载，需要从items.py中取哪一项 front_image_url对应于item中                 
        IMAGES_URLS_FIELD = [front_image_url]      ##从什么地方下载
        project_dir = os.path.dirname(os.path.abspath(__file__))
        IMAGES_STORE = os.path.join(project_dir, "images")    ## 下载图片保存到本地哪个路径
        #图片过滤规则
        IMAGES_MIN_HEIGHT = 100  #图片最小高度
        IMAGES_MIN_WIDTH = 100   #图片最小宽度
        
                         
        在spiders/jobbole.py中回调函数 yield article_item(Items),会直接跳转到settings.py设置的item_pipeline
        管道中,:num,num越小越先被调用，所以ImagesPipeline要比ArticlespiderPipeline先调用
        
    2.安装PIL模块
       (虚拟环境下)>  pip install -i  https://pypi.douban.com/simple/ pillow
       
    3.需要将jobbole.py中
             article_item["front_image_url"] = front_image_url
             该为
             article_item["front_image_url"] = [front_image_url]

```

## scrapy 将item 转化为 json文件
```shell
    1.
        from scrapy.exporters import JsonItemExporter
        
    2.在pipeline.py 中定义
    
            class JsonExporterPipeline(object):
                # 调用scrapy提供的json exporter 导出json文件
                def __init__(self):
                    self.file = open("article_exporter.json", "wb")
                    self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
                    self.exporter.start_exporting()
            
                def close_spider(self, spider):
                    self.exporter.finish_exporting()
                    self.file.close()
            
                def process_item(self, item, spider):
                    self.exporter.export_item(item)
                    return item
```

## scrapy ItemLoader

```shell
    1.目的
        主要是在 jobbole.py文件中对xpath,以及css的重写,使得css样式(.entry-header h1::text)不再是硬编码到程序中,
        而是根据数据库进行动态的加载 css样式
        
        (1) 调用顺序
                先在jobbole.py中运行item_loader.load_item()，这个时候调用了items.py文件中的
                JobBoleArticleItem()中的预处理函数(input_processor),以及output_processor
        
    2.在jobbole.py文件中
        from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
        
         # 通过item Loader 来加载 item
        # 首先定义itemLoader 的实例
        # ItemLoader()函数有2个重要的参数
        # 第一个参数 item对应于  items.py中的JobBoleArticleItem()
        # 第二个参数是 response

        # 为了能够自动取list的第一个元素,我们自定义了ArticleItemLoader 继承 ItemLoader
        #    class ArticleItemLoader(ItemLoader):
        #    #自定义ItemLoader
        #    ## 实际上只取list第一个元素
        #       default_output_processor = TakeFirst()
        
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)

        #item_loader.add_css() 是通过网页中的样式进行提取,为 item_loader添加规则
        # 用add_css()方法的好处是 其代码较为清晰,并且参数css的样式可以通过对数据库查找动态的加载,而
        # 不是硬编码到程序中，方便进行动态配置
        # 第一个参数为item中 选项值
        # 第二个参数为css的样式
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_css("context", ".entry")
        item_loader.add_css("datetime", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_css("like_num", ".vote-post-up h10::text")
        item_loader.add_css("collect_num", ".bookmark-btn::text")
        item_loader.add_css("context", ".entry")

        # 如果不是通过css的样式取出对应的值,则使用 item_loader.add_value
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url", [front_image_url])

        # 调用 load_item() 方法,才会将 前面的规则进行解析
        # 这里会调用JobBoleArticleItem()中的预处理函数(input_processor),以及output_processor
        article_item = item_loader.load_item()
        
    3.在items.py 中
        from datetime import datetime
        # MapCompose类可以将我们对item调用任何多的函数，主要解决对item中各个字段进行处理
        # TakeFirst 类 主要取list数组中的第一个元素
        from scrapy.loader.processors import MapCompose,TakeFirst
        # 对于自定义ArticleItemLoader类的重载
        from scrapy.loader import ItemLoader
        
        # 正则表达式
        import re
        
        def date_convert(value):
            try:
                create_date = datetime.strptime(value, "%Y/%m/%d").date()
            except Exception as e:
                create_date = datetime.now().date()
        
            return create_date
        
        def get_nums(value):
            match_var = re.match(r'.*?(\d+).*', value)
            if match_var:
                num = int(match_var.group(1))
            else:
                num = 0
            return num
        
        ## 为了不需要对每一个item字段都进行output_processor = TakeFirst(),我们可以自己定义itemLoader
        class ArticleItemLoader(ItemLoader):
            #自定义ItemLoader
            ## 实际上只取list第一个元素
            default_output_processor = TakeFirst()
        
        # 这个JobBoleArticleItem达到了对代码的重用
        class JobBoleArticleItem(scrapy.Item):
        
            # input_processor 含义是 当 item 的 title字段的值传递进来的时候，可以对传递进来的值进行预处理
            # MapCompose 函数 可以传入多个函数变量
            title = scrapy.Field(
                input_processor = MapCompose(add_jobbole, lambda x:x + " ")
            )             # 标题
            datetime = scrapy.Field(
                input_processor=MapCompose(date_convert),
                # ## 实际上只取list第一个元素
                # output_processor = TakeFirst()  # 因为自定义了 ArticleItemLoader
            )          # 发表日期
            like_num = scrapy.Field(
                input_processor=MapCompose(get_nums)
            )          # 点赞数
            url = scrapy.Field()               # 对应的url
            url_object_id = scrapy.Field()      # 对应的url的md5
            front_image_url = scrapy.Field(
                # 这里必须为list
                output_processor=MapCompose(return_value)
            )   # 存放文章封面图
            front_image_path = scrapy.Field()  # 存放文章封面图的本地路径
            collect_num = scrapy.Field(
                input_processor=MapCompose(get_nums)
            )       # 收藏数
        
            context = scrapy.Field()           # 正文
            
    4.在items.py 中如果 class JobBoleArticleItem 中接受的字段有 list类型(tag)需要将其join为str
            
             from scrapy.loader.processors import Join
             
            # 定义一个函数将tags中 "评论" 字符串去掉 
            def remove_comment_tags(value):
                if "评论" in value:
                    return ""
                else
                    return value
            class JobBoleArticleItem(scrapy.Item):
                tags = scrapy.Field(
                    input_processor=MapCompose(remove_comment_tags),
                    # 第一个参数是连接符(",")
                    output_processor=Join(",")
                )
                
```