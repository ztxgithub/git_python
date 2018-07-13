# python 数据库访问
 
## SQLite

```shell

    1.# 导入SQLite驱动:
      >>> import sqlite3
      # 连接到SQLite数据库
      # 数据库文件是test.db
      # 如果文件不存在，会自动在当前目录创建:
      >>> conn = sqlite3.connect('test.db')
      # 创建一个Cursor:
      >>> cursor = conn.cursor()
      # 执行一条SQL语句，创建user表:
      >>> cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
      <sqlite3.Cursor object at 0x10f8aa260>
      # 继续执行一条SQL语句，插入一条记录:
      >>> cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
      <sqlite3.Cursor object at 0x10f8aa260>
      # 通过rowcount获得插入的行数:
      >>> cursor.rowcount
      1
      # 关闭Cursor:
      >>> cursor.close()
      # 提交事务:
      >>> conn.commit()
      # 关闭Connection:
      >>> conn.close()
      
      查询记录:
        >>> conn = sqlite3.connect('test.db')
        >>> cursor = conn.cursor()
        # 执行查询语句:
        >>> cursor.execute('select * from user where id=?', ('1',))
        <sqlite3.Cursor object at 0x10f8aa340>
        # 获得查询结果集:
        >>> values = cursor.fetchall()
        >>> values
        [('1', 'Michael')]
        >>> cursor.close()
        >>> conn.close()
        
    2.使用Cursor对象执行insert，update，delete语句时，执行结果由rowcount返回影响的行数，就可以拿到执行结果
      使用Cursor对象执行select语句时，通过featchall()可以拿到结果集。结果集是一个list，每个元素都是一个tuple，对应一行记录
      如果SQL语句带有参数，那么需要把参数按照位置传递给execute()方法，有几个?占位符就必须对应几个参数，例如：
      cursor.execute('select * from user where name=? and pwd=?', ('abc', 'password'))

```

## MySQL
### 数据库驱动安装

```shell
    (1) windows 系统:
             (article_spider) D:\Program Files\PowerCmd>pip install mysqlclient
             
    (2) Ubuntu系统:
            > sudo apt-get install libmysqlclient-devsimp
            
    (3) Centos系统:
            > sudo yum install python-devel mysql-devel
            
```

### 使用
```shell
    1.# 导入MySQL驱动:
      >>> import mysql.connector
      # 注意把password设为你的root口令:
      >>> conn = mysql.connector.connect(user='root', password='password', database='test')
      >>> cursor = conn.cursor()
      # 创建user表:
      >>> cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
      # 插入一行记录，注意MySQL的占位符是%s:
      >>> cursor.execute('insert into user (id, name) values (%s, %s)', ['1', 'Michael'])
      >>> cursor.rowcount
      1
      # 提交事务:
      >>> conn.commit()
      >>> cursor.close()
      # 运行查询:
      >>> cursor = conn.cursor()
      >>> cursor.execute('select * from user where id = %s', ('1',))
      >>> values = cursor.fetchall()
      >>> values
      [('1', 'Michael')]
      # 关闭Cursor和Connection:
      >>> cursor.close()
      True
      >>> conn.close()
      
      执行INSERT等操作后要调用commit()提交事务；
      
      MySQL的SQL占位符是%s
      
      
    2.
        (1) import MySQLdb
        (2) 
        #将数据保存到数据库中
            class MysqlPipeline(object):
                def __init__(self):
                    ## 刚开始进行数据库的连接
                    self.conn = MySQLdb.connect(host='127.0.0.1', user='root', password='123456',
                                                database='article_spider', charset="utf8", 
                                                use_unicode=True)
                    self.cursor = self.conn.cursor()
            
                def process_item(self, item, spider):
                    insert_sql = """
                        insert into jobbole_article(title, datetime, url, 
                        url_object_id, front_image_url, front_image_path, like_num, collect_num, context)
                        values(%s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
            
                    self.cursor.execute(insert_sql, (item["title"], item["datetime"], item["url"],
                                                     item["url_object_id"], item["front_image_url"],
                                                     item["front_image_path"], item["like_num"],
                                                     item["collect_num"], item["context"]))
                    self.conn.commit()
                    
        注意：
            这种数据库插入的操作是同步的，当程序的对数据的解析速度超过数据库的写入速度，则数据库会发生大量的
            堵塞。
            
    3.Twisted框架下更高效的数据库操作
        提供了连接池，将Mysql的操作变为异步操作，目前 Twisted 支持的是关系型数据库
        除了在MySQLdb.connect进行基本配置外，在scrapy框架中还可以在 settings.py中进行数据库连接的相关配置。
        
        (1) 在 settings.py 文件中写入
                MYSQL_HOST = "127.0.0.1"
                MYSQL_DBNAME = "article_spider"
                MYSQL_USER = "root"
                MYSQL_PASSWORD = "123456"
                
        (2) 在pipelines.py文件中
                ##这个adbapi能够将我们的数据库操作变为异步化的操作
                from twisted.enterprise import adbapi
                import MySQLdb
                import MySQLdb.cursors
                
                
             #通过twisted框架进行数据库插入
            class MysqlTwistedPipeline(object):
            
                def __init__(self, dbpool):
                    self.dbpool = dbpool
            
                @classmethod
                def from_settings(cls, settings):
                    ## dict 里面的参数名称 例如 ”database"这些要与MySQLdb.connect函数中的固定参数名要一致
                    dbparams = dict(
                        host = settings["MYSQL_HOST"],
                        database = settings["MYSQL_DBNAME"],
                        user = settings["MYSQL_USER"],
                        password = settings["MYSQL_PASSWORD"],
                        charset= 'utf8',
                        cursorclass = MySQLdb.cursors.DictCursor,
                        use_unicode=True
                    )
            
                    ## twisted 本身使用时异步的容器，具体操作还是对应的数据库
                    ## "MySQLdb" 对应于 数据库的模块名
                    ## *connargs 是数据库连接的参数
                    dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
                    return cls(dbpool)
            
                # 使用twisted将mysql插入变为异步执行
                def process_item(self, item, spider):
                    ## 调用twisted 中的runInteraction函数来执行异步操作
                    query = self.dbpool.runInteraction(self.do_insert, item)
                    ##进行错误的处理判断
                    query.addErrback(self.handle_error)
            
                def handle_error(self, failure):
                    #处理异步插入的异常
                    print(failure)
            
                def do_insert(self, cursor, item):
                    #执行具体得插入
                    insert_sql = """
                                insert into jobbole_article(title, datetime, url, 
                                url_object_id, front_image_url, front_image_path, 
                                like_num, collect_num, context)
                                values(%s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """
            
                    cursor.execute(insert_sql, (item["title"], item["datetime"], item["url"],
                                                     item["url_object_id"], item["front_image_url"],
                                                     item["front_image_path"], item["like_num"],
                                                     item["collect_num"], item["context"]))
                    ## 不需要commit twisted自动帮我们commit
                                    
    4.github 上 scrapy-djangoitem
    5.
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

```

