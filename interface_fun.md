# python 接口函数
 
- range()函数

```shell

    可以生成一个整数序列,range(5)生成的序列是从0开始小于5的整数(0,1,2,3,4)
    >>> list(range(5))
        [0, 1, 2, 3, 4]

```

- 数据类型转换

```shell

   (1) >>> int('123')
        123
        
   (2) >>> int(12.34)
        12
   (3) >>> float('12.34')
        12.34
   (4) >>> str(1.23)
        '1.23'
   (5) >>> str(100)
        '100'
   (6) >>> bool(1)
        True
   (7) >>> bool('')
        False

```

- isinstance() : 数据类型检查

```shell

   def my_abs(x):
       if not isinstance(x, (int, float)):
           raise TypeError('bad operand type')
       if x >= 0:
           return x
       else:
           return -x
           
    1.isinstance()判断的是一个对象是否是该类型本身，或者位于该类型的父继承链上

```

- list(Iterator) 函数

```shell

    通过list()函数让它把惰性序列序列(Iterator )都计算出来并返回一个list

```

- type()函数

```shell

   1.判断对象类型,返回对应的Class类型
       >>> type(123)
       <class 'int'>
       >>> type('str')
       <class 'str'>
       
   2.判断一个对象是否是函数,使用types模块中定义的常量
        >>> import types
        >>> def fn():
        ...     pass
        ...
        >>> type(fn)==types.FunctionType
        True
        >>> type(abs)==types.BuiltinFunctionType
        True
        >>> type(lambda x: x)==types.LambdaType
        True
        >>> type((x for x in range(10)))==types.GeneratorType
        True
        
   3.type()函数既可以返回一个对象的类型,又可以创建出新的类型,比如,我们可以通过type()函数创建出Hello类,
     而无需通过class Hello(object)...的定义：
            >>> def fn(self, name='world'): # 先定义函数
            ...     print('Hello, %s.' % name)
            ...
            >>> Hello = type('Hello', (object,), dict(hello=fn)) # 创建Hello class
            >>> h = Hello()
            >>> h.hello()
            Hello, world.
            >>> print(type(Hello))
            <class 'type'>
            >>> print(type(h))
            <class '__main__.Hello'>
            
         要创建一个class对象，type()函数依次传入3个参数：
            1.class的名称；
            2.继承的父类集合，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法；
            3.class的方法名称与函数绑定，这里我们把函数fn绑定到方法名hello上。
            
     通过type()函数创建的类和直接写class是完全一样的，因为Python解释器遇到class定义时，
     仅仅是扫描一下class定义的语法，然后调用type()函数创建出class.
     正常情况下，我们都用class Xxx...来定义类，但是，type()函数也允许我们动态创建出类来,
     也就是说，动态语言本身支持运行期动态创建类
```

- dir()函数

```shell

   1.获得一个对象的所有属性和方法,返回一个包含字符串的list,
     比如，获得一个str对象的所有属性和方法
        >>> dir('ABC')
        ['__add__', '__class__',..., '__subclasshook__', 'capitalize', 'casefold',..., 'zfill']
    
```

- hasattr()函数

```shell

   1.查看对象是否有 相应的属性
        >>> hasattr(obj, 'x') # 有属性'x'吗？
        True
        
   一个合适的用法的例子如下：
        def readImage(fp):
            if hasattr(fp, 'read'):
                return readData(fp)
            return None
            
        假设我们希望从文件流fp中读取图像，我们首先要判断该fp对象是否存在read方法，如果存在，
        则该对象是一个流，如果不存在，则无法读取。hasattr()就派上了用场。
```

- setattr()函数

```shell

   1.对对象设置 相应的属性(可以是新增)
        >>> hasattr(obj, 'y') # 有属性'y'吗？
        False
        >>> setattr(obj, 'y', 19) # 设置一个属性'y'
        >>> hasattr(obj, 'y') # 有属性'y'吗？
        True
```

- getattr()函数

```shell

   1.获取对象相应的属性值
        >>> getattr(obj, 'y') # 获取属性'y'
        19
        >>> obj.y # 获取属性'y'
        19
        
   2.如果试图获取不存在的属性,会抛出AttributeError的错误
        >>> getattr(obj, 'z') # 获取属性'z'
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        AttributeError: 'MyObject' object has no attribute 'z'
        
   3.可以传入一个default参数，如果属性不存在，就返回默认值
        >>> getattr(obj, 'z', 404) # 获取属性'z'，如果不存在，返回默认值404
        404
```

- super继承

```shell

   1.super 是用来解决多重继承问题的,直接用类名调用父类方法在使用单继承的时候没问题，但是如果使用多继承，
     会涉及到查找顺序（MRO）、重复调用（钻石继承）等种种问题
   2.在super机制里可以保证公共父类仅被执行一次
   3.注意super继承只能用于新式类，用于经典类时就会报错
        新式类：必须有继承的类，如果没什么想继承的，那就继承object
        经典类：没有父类，如果此时调用super就会出现错误：『super() argument 1 must be type, not classobj』
        # 经典类
        class A():
            def __init__(self):
                print 'A'
        
        class B(A):
            def __init__(self):
                A.__init__(self)
                print 'B'
        
        class C(B, A):
            def __init__(self):
                A.__init__(self)
                B.__init__(self)
                print 'C'
                
        # 新式类
        class A(object):
            def __init__(self):
                print 'A'
        
        class B(A):
            def __init__(self):
                super(B, self).__init__()
                print 'B'
        
        class C(B, A):
            def __init__(self):
                super(C, self).__init__()
                print 'C'
                
        采用新式类，要求最顶层的父类一定要继承于object，这样就可以利用super()函数来调用父类的init()等函数，
        每个父类都执行且执行一次，并不会出现重复调用的情况。而且在子类的实现中，不用到处写出所有的父类名字，符合DRY原则
        采用super()方式时，会自动找到第一个多继承中的第一个父类，
        但是如果还想强制调用其他父类的init()函数或两个父类的同名函数时，就要用老办法了。
        
```

## random模块

- random.uniform()

```shell

    函数原型为：random.uniform(a, b)
    描述:
        用于生成一个指定范围内的随机符点数，两个参数其中一个是上限，一个是下限
```

## 文件相关函数

- open()函数

```shell

    1.读取二进制文件，比如图片、视频等等，用'rb'模式打开文件即可
            >>> f = open('/Users/michael/test.jpg', 'rb')
    2.要读取非UTF-8编码的文本文件,需要给open()函数传入encoding参数，例如，读取GBK编码的文件
            >>> f = open('/Users/michael/gbk.txt', 'r', encoding='gbk')
            >>> f.read()
            '测试'
            
    3.遇到有些编码不规范的文件，你可能会遇到UnicodeDecodeError，因为在文本文件中可能夹杂了一些非法编码的字符。遇到这种情况，
      open()函数还接收一个errors参数，表示如果遇到编码错误后如何处理。最简单的方式是直接忽略：
            >>> f = open('/Users/michael/gbk.txt', 'r', encoding='gbk', errors='ignore')
            
    参数:
        'w'模式 :覆盖写
        'a'  : 以追加（append）模式写入
```

- read()函数

```shell

   str read():一次性读取文件的全部内容   
   str read(size) :一次最多读size个字节
   str readline():每次读取一行内容
```

## 字符串函数

- str.strip() :把末尾的'\n'删掉

- join 函数
```shell
    1.对应字符串的join，第二个参数为list，则在形成字符串中,每个list元素加上join的第一个参数
        >>> tag_list = ["123","345","111"]
        >>> tag_list
            ['123', '345', '111']
        >>> tag_list = ",".join(tag_list)
        >>> tag_list
            '123,345,111'
```