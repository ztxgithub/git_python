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

```

