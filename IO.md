# python IO
 
## IO同步编程

### 文件读写

```shell
    1.读文件
        (1) >>> f = open('/Users/michael/test.txt', 'r')
        (2) 调用read()方法可以一次读取文件的全部内容，Python把内容读到内存，用一个str对象表示
            >>> f.read()  ()
        (3) >>> f.close()
        
        为了保证无论是否出错都能正确地关闭文件，我们可以使用try ... finally来实现：
            try:
                f = open('/path/to/file', 'r')
                print(f.read())
            finally:
                if f:
                    f.close()
                    
        引入了with语句来自动帮我们调用close()方法：
            with open('/path/to/file', 'r') as f:
                print(f.read())
                
    2.file-like Object
        1.像open()函数返回的这种有个read()方法的对象，在Python中统称为file-like Objec
        2.StringIO就是在内存中创建的file-like Object，常用作临时缓冲
    3.写文件
        当我们写文件时,操作系统往往不会立刻把数据写入磁盘,而是放到内存缓存起来，空闲的时候再慢慢写入。
        只有调用close()方法时，操作系统才保证把没有写入的数据全部写入磁盘
                with open('/Users/michael/test.txt', 'w') as f:
                    f.write('Hello, world!')

```

### StringIO和BytesIO

```shell
    1.StringIO
        (1) 在内存中读写str,要把str写入StringIO，我们需要先创建一个StringIO，然后，像文件一样写入即可：
                >>> from io import StringIO
                >>> f = StringIO()
                >>> f.write('hello')
                5
                >>> f.write(' ')
                1
                >>> f.write('world!')
                6
                >>> print(f.getvalue())
                hello world!
                
                getvalue()方法用于获得写入后的str。
                
        (2) 读取StringIO
                >>> from io import StringIO
                >>> f = StringIO('Hello!\nHi!\nGoodbye!')
                >>> while True:
                ...     s = f.readline()
                ...     if s == '':
                ...         break
                ...     print(s.strip())
                ...
                Hello!
                Hi!
                Goodbye!
                
    2.BytesIO
        (1) BytesIO实现了在内存中写bytes，我们创建一个BytesIO，然后写入一些bytes：
                >>> from io import BytesIO
                >>> f = BytesIO()
                >>> f.write('中文'.encode('utf-8'))  ### 经过UTF-8编码的bytes。
                6
                >>> print(f.getvalue())
                b'\xe4\xb8\xad\xe6\x96\x87'
                
        (2) BytesIO的读
            >>> from io import BytesIO
            >>> f = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
            >>> f.read()
            b'\xe4\xb8\xad\xe6\x96\x87'
   
```

### 序列化

```shell
    1.从内存中变成可存储或传输的过程称之为序列化,在Python中叫pickling，在其他语言中也被称之为serialization，marshalling,
      flattening等等，都是一个意思
      
    2.Python提供了pickle模块来实现序列化。
        一个对象序列化并写入文件:
            >>> import pickle
            >>> d = dict(name='Bob', age=20, score=88)
            >>> pickle.dumps(d)
            b'\x80\x03}q\x00(X\x03\x00\x00\x00ageq\x01K\x14X\x05\x00\x00\x00scoreq\x02KXX\x04\x00\x00\x00nameq\x03X\x03\x00\x00\x00Bobq\x04u.'
   
            >>> f = open('dump.txt', 'wb')
            >>> pickle.dump(d, f)
            >>> f.close()
            
        反序列化为对象
            当我们要把对象从磁盘读到内存时，可以先把内容读到一个bytes，然后用pickle.loads()方法反序列化出对象，
            也可以直接用pickle.load()方法从一个file-like Object中直接反序列化出对象。
            我们打开另一个Python命令行来反序列化刚才保存的对象:
                >>> f = open('dump.txt', 'rb')
                >>> d = pickle.load(f)
                >>> f.close()
                >>> d
                {'age': 20, 'score': 88, 'name': 'Bob'}
                
        注意:
            Pickle的问题和所有其他编程语言特有的序列化问题一样，就是它只能用于Python，并且可能不同版本的Python彼此都不兼容
            
    3.JSON
        如果我们要在不同的编程语言之间传递对象，就必须把对象序列化为标准格式,比如JSON格式
        Python内置的json模块提供了非常完善的Python对象到JSON格式的转换。
        
        
        dict的序列化:
            JSON序列化:
            我们先看看如何把Python对象变成一个JSON：
                >>> import json
                >>> d = dict(name='Bob', age=20, score=88)
                >>> json.dumps(d)
                '{"age": 20, "score": 88, "name": "Bob"}'
                
            (1) 注意如果json中存在中文将参数ensure_ascii改为False
                    json.dumps(dict(item), ensure_ascii=False)
                
            JSON反序列化:
                >>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
                >>> json.loads(json_str)
                {'age': 20, 'score': 88, 'name': 'Bob'}
                
        其他数据类型的序列化:
            序列化:
                A.例如 class对象
                    import json
                    
                    class Student(object):
                        def __init__(self, name, age, score):
                            self.name = name
                            self.age = age
                            self.score = score
                B.需要为Student专门写一个转换函数，再把函数传到dumps方法中进去即可
                        def student2dict(std):
                            return {
                                'name': std.name,
                                'age': std.age,
                                'score': std.score
                            }
                C.Student实例首先被student2dict()函数转换成dict，然后再被顺利序列化为JSON
                    >>> print(json.dumps(s, default=student2dict))
                    {"age": 20, "name": "Bob", "score": 88}
                    
                 还有一种方法:  
                    把任意class的实例变为dict：
                    
                    print(json.dumps(s, default=lambda obj: obj.__dict__))
                    
            反序列化:
                如果我们要把JSON反序列化为一个Student对象实例,loads()方法首先转换出一个dict对象，然后，
                我们将定义好的dict转换为Student对象函数赋值给loads方法中object_hook函数:
                    def dict2student(d):
                        return Student(d['name'], d['age'], d['score'])
                        
                    >>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
                    >>> print(json.loads(json_str, object_hook=dict2student))
                    <__main__.Student object at 0x10cd3c190>
                  
```

## 异步IO

### 概要
```shell
    1.事件驱动模型:Nginx就是支持异步IO的Web服务器，它在单核CPU上采用单进程模型就可以高效地支持多任务
    2.对应到Python语言，单线程的异步编程模型称为协程，有了协程的支持，就可以基于事件驱动编写高效的多任务程序
```