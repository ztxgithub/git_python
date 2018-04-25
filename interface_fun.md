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