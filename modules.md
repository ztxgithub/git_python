# python 模块
 
## pyhton 模块概念

```shell

    1.一个.py文件就称之为一个模块（Module）
    2.使用模块还可以避免函数名和变量名冲突。相同名字的函数和变量完全可以分别存在不同的模块中，
      因此，我们自己在编写模块时，不必考虑名字会与其他模块冲突。但是也要注意，尽量不要与内置函数名字冲突
      
    3.避免模块名冲突，Python又引入了按目录来组织模块的方法，称为包（Package）
      假设我们的abc和xyz这两个模块名字与其他模块冲突了,于是我们可以通过包来组织模块，避免冲突.
      方法是选择一个顶层包名，比如mycompany
      引入了包以后，只要顶层的包名不与别人冲突,那所有模块都不会与别人冲突。现在，
      abc.py模块的名字就变成了mycompany.abc，类似的，xyz.py的模块名变成了mycompany.xyz
      每一个包目录下面都会有一个__init__.py的文件，这个文件是必须存在的，否则，Python就把这个目录当成普通目录，
      而不是一个包。__init__.py可以是空文件，也可以有Python代码，因为__init__.py本身就是一个模块，
      而它的模块名就是mycompany.
      
    4. 自己创建模块时要注意命名,不能和Python自带的模块名称冲突。例如，系统自带了sys模块，自己的模块就不可命名为sys.py,
       否则将无法导入系统自带的sys模块。

```

## 使用模块

```shell

    1.
        #!/usr/bin/env python3
        # -*- coding: utf-8 -*-
        
        ' a test module '            (一个字符串，表示模块的文档注释，任何模块代码的第一个字符串都被视为模块的文档注释；)
        
        __author__ = 'Michael Liao'
        
        import sys    (我们就有了变量sys指向该模块，利用sys这个变量，就可以访问sys模块的所有功能)
        
        def test():
            args = sys.argv
            if len(args)==1:
                print('Hello, world!')
            elif len(args)==2:
                print('Hello, %s!' % args[1])
            else:
                print('Too many arguments!')
        
        if __name__=='__main__':
            test()
            
            
        当我们在命令行运行hello模块文件时，Python解释器把一个特殊变量__name__置为__main__，
        而如果在其他地方导入该hello模块时，if判断将失败，因此，这种if测试可以让一个模块通过命令行运行时执行一些额外的代码，
        最常见的就是运行测试。
        
        A.启动Python交互环境，再导入hello模块
                $ python3
                Python 3.4.3 (v3.4.3:9b73f1c3e601, Feb 23 2015, 02:52:03) 
                [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
                Type "help", "copyright", "credits" or "license" for more information.
                >>> import hello   (导入时，没有打印Hello, word!，因为没有执行test()函数)
                >>> hello.test()    (调用hello.test()时，才能打印出Hello, word!)
                结果
                Hello, world!
                
    2.作用域
        在一个模块中,我们可能会定义很多函数和变量,但有的函数和变量我们希望给别人使用，
        有的函数和变量我们希望仅仅在模块内部使用。在Python中，是通过_前缀来实现的
        类似_xxx和__xxx这样的函数或变量就是非公开的（private），不应该被直接引用，比如_abc，__abc等

```

## 安装第三方模块

```shell

    1.在Python中，安装第三方模块，是通过包管理工具pip完成的
    2.Linux上有可能并存Python 3.x和Python 2.x，因此对应的pip命令是pip3
    3.要安装一个第三方库，必须先知道该库的名称，可以在官网或者pypi上搜索，比如Pillow的名称叫Pillow，
      因此，安装Pillow的命令就是：
        > pip install Pillow
        
    4.安装常用模块,推荐直接使用Anaconda，这是一个基于Python的数据处理和科学计算平台，它已经内置了许多非常有用的第三方库，
      我们装上Anaconda，就相当于把数十个第三方模块自动安装好了，非常简单易用。
      
    5.模块搜索路径
       A.Python解释器会搜索当前目录、所有已安装的内置模块和第三方模块，搜索路径存放在sys模块的path变量中
            >>> import sys
            >>> sys.path
            
       B.如果我们要添加自己的搜索目录
            (1) 直接修改sys.path，添加要搜索的目录 这种方法是在运行时修改，运行结束后失效:
                    >>> import sys
                    >>> sys.path.append('/Users/michael/my_py_scripts')
            (2) windows设置环境变量PYTHONPATH，该环境变量的内容会被自动添加到模块搜索路径中。
                设置方式与设置Path环境变量类似。注意只需要添加你自己的搜索路径，Python自己本身的搜索路径不受影响

```

## 内建模块

### datetime

```shell

    1.datetime是Python处理日期和时间的标准库
        from datetime import datetime, timedelta, timezone
        
        datetime(year,month,day,hour,minute,second,us)
          
    2.获取当前日期和时间
        >>> from datetime import datetime
        >>> now = datetime.now() # 获取当前datetime
        >>> print(now)
        2015-05-18 16:28:07.198690
        >>> print(type(now))
        <class 'datetime.datetime'>
        
        注意到datetime是模块，datetime模块还包含一个datetime类，通过from datetime import datetime导入的才是datetime这个类。
        
        如果仅导入import datetime，则必须引用全名datetime.datetime。
        
        datetime.now()返回当前日期和时间，其类型是datetime。
        
    3.获取指定日期和时间
        >>> from datetime import datetime
        >>> dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
        >>> print(dt)
        2015-04-19 12:20:00
        
    4.datetime转换为timestamp
    
        >>> from datetime import datetime
        >>> dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
        >>> dt.timestamp() # 把datetime转换为timestamp
        1429417200.0
        
        小数位表示毫秒数
        
    5.timestamp转换为datetime
        注意到timestamp是一个浮点数,它没有时区的概念，而datetime是有时区的。转换是在timestamp和本地时间做转换
        
        >>> from datetime import datetime
        >>> t = 1429417200.0
        >>> print(datetime.fromtimestamp(t)) # 本地时间
        2015-04-19 12:20:00
        >>> print(datetime.utcfromtimestamp(t)) # UTC时间
        2015-04-19 04:20:00
        
    6.str转换为datetime
        需要一个日期和时间的格式化字符串,转换后的datetime是没有时区信息的
        >>> from datetime import datetime
        >>> cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
        >>> print(cday)
        2015-06-01 18:19:59
        
    7.datetime转换为str
        格式化字符串:https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        >>> from datetime import datetime
        >>> now = datetime.now()
        >>> print(now.strftime('%a, %b %d %H:%M'))
        Mon, May 05 16:28
        
    8.datetime加减
        加减可以直接用+和-运算符，不过需要导入timedelta这个类
            >>> from datetime import datetime, timedelta
            >>> now = datetime.now()
            >>> now
            datetime.datetime(2015, 5, 18, 16, 57, 3, 540997)
            >>> now + timedelta(hours=10)
            datetime.datetime(2015, 5, 19, 2, 57, 3, 540997)
            >>> now - timedelta(days=1)
            datetime.datetime(2015, 5, 17, 16, 57, 3, 540997)
            >>> now + timedelta(days=2, hours=12)
            datetime.datetime(2015, 5, 21, 4, 57, 3, 540997)
            
    9.本地时间转换为UTC时间
            本地时间是指系统设定时区的时间，例如北京时间是UTC+8:00时区的时间，而UTC时间指UTC+0:00时区的时间
            一个datetime类型有一个时区属性tzinfo，但是默认为None，所以无法区分这个datetime到底是哪个时区，
            除非强行给datetime设置一个时区：
                >>> from datetime import datetime, timedelta, timezone
                >>> tz_utc_8 = timezone(timedelta(hours=8)) # 创建时区UTC+8:00
                >>> now = datetime.now()
                >>> now
                datetime.datetime(2015, 5, 18, 17, 2, 10, 871012)
                >>> dt = now.replace(tzinfo=tz_utc_8) # 强制设置为UTC+8:00
                >>> dt
                datetime.datetime(2015, 5, 18, 17, 2, 10, 871012, tzinfo=datetime.timezone(datetime.timedelta(0, 28800)))
                
            如果系统时区恰好是UTC+8:00，那么上述代码就是正确的，否则，不能强制设置为UTC+8:00时区
    10.时区转换
            通过utcnow()拿到当前的UTC时间，再转换为任意时区的时间
            时区转换的关键在于，拿到一个datetime时，要获知其正确的时区，然后强制设置时区，作为基准时间
            利用带时区的datetime，通过astimezone()方法，可以转换到任意时区。
            注：不是必须从UTC+0:00时区转换到其他时区，任何带时区的datetime都可以正确转换，例如上述bj_dt到tokyo_dt的转换。
               在经过astimezone函数时,从bj_dt到tokyo_dt的转换,其
               tokyo_dt2 = bj_dt.astimezone(timezone(timedelta(hours=9)))
               这里hours是与utc的差值
               
            # 拿到UTC时间，并强制设置时区为UTC+0:00:
            >>> utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
            >>> print(utc_dt)
            2015-05-18 09:05:12.377316+00:00
            # astimezone()将转换时区为北京时间:
            >>> bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
            >>> print(bj_dt)
            2015-05-18 17:05:12.377316+08:00
            # astimezone()将转换时区为东京时间:
            >>> tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))
            >>> print(tokyo_dt)
            2015-05-18 18:05:12.377316+09:00
            # astimezone()将bj_dt转换时区为东京时间:
            >>> tokyo_dt2 = bj_dt.astimezone(timezone(timedelta(hours=9)))
            >>> print(tokyo_dt2)
            2015-05-18 18:05:12.377316+09:00
            
            
    11.datetime表示的时间需要时区信息才能确定一个特定的时间，否则只能视为本地时间。
       如果要存储datetime，最佳方法是将其转换为timestamp再存储，因为timestamp的值与时区完全无关。

```

### collections

```shell

    1.namedtuple
        namedtuple是一个函数,它用来创建一个自定义的tuple对象，并且规定了tuple元素的个数，
        并可以用属性而不是索引来引用tuple的某个元素
        我们用namedtuple可以很方便地定义一种数据类型，它具备tuple的不变性，又可以根据属性来引用，使用十分方便.
        
        >>> from collections import namedtuple
        >>> Point = namedtuple('Point', ['x', 'y'])
        >>> p = Point(1, 2)
        >>> p.x
        1
        >>> p.y
        2
        
       (1) 用坐标和半径表示一个圆，也可以用namedtuple定义：
                # namedtuple('名称', [属性list]):
                Circle = namedtuple('Circle', ['x', 'y', 'r'])
                
    2.deque
        deque是为了高效实现插入和删除操作的双向列表，适合用于队列和栈,
        deque除了实现list的append()和pop()外，还支持appendleft()和popleft()，
        这样就可以非常高效地往头部添加或删除元素。
        
        >>> from collections import deque
        >>> q = deque(['a', 'b', 'c'])
        >>> q.append('x')
        >>> q.appendleft('y')
        >>> q
        deque(['y', 'a', 'b', 'c', 'x'])
        
    3.defaultdict 
        使用dict时,如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用defaultdict  
        默认值是调用函数返回的，而函数在创建defaultdict对象时传入
        
            >>> from collections import defaultdict
            >>> dd = defaultdict(lambda: 'N/A')
            >>> dd['key1'] = 'abc'
            >>> dd['key1'] # key1存在
            'abc'
            >>> dd['key2'] # key2不存在，返回默认值
            'N/A'
            
    4.OrderedDict
        使用dict时，Key是无序的,如果要保持Key的顺序，可以用OrderedDict
        注意:OrderedDict的Key会按照插入的顺序排列，不是Key本身排序：
            >>> from collections import OrderedDict
            >>> d = dict([('a', 1), ('b', 2), ('c', 3)])
            >>> d # dict的Key是无序的
            {'a': 1, 'c': 3, 'b': 2}
            >>> od = OrderedDict([('a', 1), ('d', 2), ('c', 3)])
            >>> od # OrderedDict的Key是有序的
            OrderedDict([('a', 1), ('d', 2), ('c', 3)])
            
            OrderedDict可以实现一个FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key:
            
                from collections import OrderedDict
                
                class LastUpdatedOrderedDict(OrderedDict):
                
                    def __init__(self, capacity):
                        super(LastUpdatedOrderedDict, self).__init__()
                        self._capacity = capacity
                
                    def __setitem__(self, key, value):
                        containsKey = 1 if key in self else 0
                        if len(self) - containsKey >= self._capacity:
                            last = self.popitem(last=False)
                            print('remove:', last)
                        if containsKey:
                            del self[key]
                            print('set:', (key, value))
                        else:
                            print('add:', (key, value))
                        OrderedDict.__setitem__(self, key, value)
                        
                        
    5.Counter
        Counter是一个简单的计数器,
        
        >>> from collections import Counter
        >>> c = Counter()
        >>> for ch in 'programming':
        ...     c[ch] = c[ch] + 1
        ...
        >>> c
        Counter({'g': 2, 'm': 2, 'r': 2, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'p': 1})

```

### base64

```shell

    1.Python内置的base64可以直接进行base64的编解码
        >>> import base64
        >>> base64.b64encode(b'binary\x00string')
        b'YmluYXJ5AHN0cmluZw=='
        >>> base64.b64decode(b'YmluYXJ5AHN0cmluZw==')
        b'binary\x00string'
        
    2.适合url 的base64编解码
      由于标准的Base64编码后可能出现字符+和/，在URL中就不能直接作为参数，
      所以又有一种"url safe"的base64编码，其实就是把字符+和/分别变成-和_：
        >>> base64.b64encode(b'i\xb7\x1d\xfb\xef\xff')
        b'abcd++//'
        >>> base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff')
        b'abcd--__'
        >>> base64.urlsafe_b64decode('abcd--__')
        b'i\xb7\x1d\xfb\xef\xff'
        
    3.Base64适用于小段内容的编码，比如数字证书签名、Cookie的内容等
    
```

### struct

```shell

    1.struct模块来解决bytes和其他二进制数据类型的转换
        > 表示字节顺序是big-endian，也就是网络序
        < 表示字节顺序是little-endian，
        c:一个字节
        I:4字节无符号整数
        H：2字节无符号整数
    2.struct的pack函数把任意数据类型变成bytes
        >>> import struct
        >>> struct.pack('>I', 10240099)
        b'\x00\x9c@c'
        
    3.struct.pack()函数
        pack的第一个参数是处理指令
            '>I'的意思是： >表示字节顺序是big-endian，也就是网络序，I表示4字节无符号整数。
            
    4.unpack把bytes变成相应的数据类型
        >>> struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80')
        (4042322160, 32896)
        根据>IH的说明，后面的bytes依次变为I：4字节无符号整数 和 H：2字节无符号整数。
    
```

### hashlib

```shell

    1.Python的hashlib提供了常见的摘要算法，如MD5，SHA1等等。
      摘要算法又称哈希算法、散列算法。它通过一个函数，把任意长度的数据转换为一个长度固定的数据串（通常用16进制的字符串表示）
      摘要算法就是通过摘要函数f()对任意长度的数据data计算出固定长度的摘要digest，目的是为了发现原始数据是否被人篡改过
      摘要算法之所以能指出数据是否被篡改过，就是因为摘要函数是一个单向函数，计算f(data)很容易，
      但通过digest反推data却非常困难。而且，对原始数据做一个bit的修改，都会导致计算出的摘要完全不同
      
    2.摘要算法MD5
        任意长度的字符串进过MD5生成结果是固定的128 bit字节，通常用一个32位的16进制字符串表示
        import hashlib
        
        md5 = hashlib.md5()
        md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
        print(md5.hexdigest())
        
        结果:
        d26a53750bc40b38b65a520292f69306
        
        (1) 数据量很大，可以分块多次调用update()，最后计算的结果是一样的
                import hashlib
                
                md5 = hashlib.md5()
                md5.update('how to use md5 in '.encode('utf-8'))
                md5.update('python hashlib?'.encode('utf-8'))
                print(md5.hexdigest())
                
    3.摘要算法SHA1
        任意长度的字符串进过SHA1生成结果是固定的160 bit字节，通常用一个40位的16进制字符串表示。
        import hashlib
        
        sha1 = hashlib.sha1()
        sha1.update('how to use sha1 in '.encode('utf-8'))
        sha1.update('python hashlib?'.encode('utf-8'))
        print(sha1.hexdigest())
        
    3.摘要算法应用
        (1) 任何允许用户登录的网站都会存储用户登录的用户名和口令,在数据库中如果保存明文,则存在安全泄露,
             正确的保存口令(密码)的方式是不存储用户的明文口令(密码)，而是存储用户口令(密码)的摘要
             当用户登录时，首先计算用户输入的明文口令的MD5，然后和数据库存储的MD5对比，
             如果一致，说明口令输入正确，如果不一致，口令肯定错误
             
        (2) 由于常用口令的MD5值很容易被计算出来，所以，要确保存储的用户口令不是那些已经被计算出来的常用口令的MD5，
            这一方法通过对原始口令加一个复杂字符串来实现，俗称“加盐”,经过Salt处理的MD5口令，只要Salt不被黑客知道，
            即使用户输入简单口令，也很难通过MD5反推明文口令：
                def calc_md5(password):
                    return get_md5(password + 'the-Salt')
        (3) 摘要算法在很多地方都有广泛的应用。要注意摘要算法不是加密算法(加密算法必定要进行解密)，不能用于加密
           （因为无法通过摘要反推明文），只能用于防篡改，但是它的单向计算特性决定了可以在不存储明文口令的情况下
           验证用户口令。
    
```