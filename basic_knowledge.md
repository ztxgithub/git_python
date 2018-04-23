# python 基础知识
 
- print()

```shell
    1.print()函数也可以接受多个字符串，用逗号“,”隔开, 遇到逗号“,”会输出一个空格
        print("hello", "world")
        结果:
            hello world
            
        print("hello" "world")
        结果:
            helloworld
```

- 对于 代码块 : 所有的代码都要缩进

```shell
    正确用法:
         for key in d:
               print(key)   这一行有tab缩进
               
    错误用法:
         for key in d:
         print(key)    这行 print在行开头,没有tab键
```
## 数据类型

### 浮点数

```shell
    1.对于很大或很小的浮点数,就必须用科学计数法表示,把10用e替代，1.23x109就是1.23e9，或者12.3e8，0.000012可以写成1.2e-5，等等
```

### 字符串

```shell
    1.用r''表示''内部的字符串默认不转义
        例如:
            >>> print(r'\t')
            结果:
                \t
                
    2.字符串内部有很多换行,用\n写在一行里不好阅读,可以用''' '''的格式表示多行内容
        例如:
            print('''hello world
            hello world2
            hello world3''')
            
        结果:
            hello world
            hello world2
            hello world3
```

### 布尔值

```shell
    1. True,False表示布尔值（请注意大小写)
    2. and、or和not运算
    3 .None 代表空值
    
```

### 变量

```shell
    1. 可以把任意数据类型赋值给变量,同一个变量可以反复赋值，而且可以是不同类型的变量
            a = 123 # a是整数
            print(a)
            a = 'ABC' # a变为字符串
            print(a)
            
    2. 变量本身类型不固定的语言称之为动态语言,与之对应的是静态语言。静态语言在定义变量时必须指定变量类型,
       如果赋值的时候类型不匹配，就会报错
    3.Python的整数没有大小限制,而C/C++语言的整数根据其存储长度是有大小限制的
```   

### 常量

```shell
    1. 常量用全部大写的变量名表示
    2. /除法计算结果是浮点数,即使是两个整数恰好整除
           (1)
                >>> 9 / 3
                结果
                3.0
           (2) 
                >>> 10 / 3
                结果
                3.3333333333333335
                
    3.// 称为地板除，两个整数的除法仍然是整数
        >>> 10 // 3
        结果
            3
```   

## 字符串和编码

### 字符编码

```shell
    1. ASCII编码是1个字节,而Unicode编码通常是2个字节。
        (1) ASCII编码
                字母A用ASCII编码是十进制的65，二进制的01000001
            
        (2) Unicode编码
                汉字 '中' Unicode编码是十进制的20013，二进制的01001110 00101101
                把ASCII编码的A用Unicode编码,只需要在前面补0就可以,因此，A的Unicode编码是00000000 01000001。
    
    2.如果你写的文本基本上全部是英文的话,用Unicode编码比ASCII编码需要多一倍的存储空间,在存储和传输上就十分不划算。
      所以,本着节约的精神,又出现了把Unicode编码转化为“可变长编码”的UTF-8编码。
      UTF-8编码把一个Unicode字符根据不同的数字大小编码成1-6个字节,常用的英文字母被编码成1个字节,汉字通常是3个字节,
      只有很生僻的字符才会被编码成4-6个字节。如果你要传输的文本包含大量英文字符，用UTF-8编码就能节省空间
      
    3.UTF-8编码有一个额外的好处,就是ASCII编码实际上可以被看成是UTF-8编码的一部分，所以，
      大量只支持ASCII编码的历史遗留软件可以在UTF-8编码下继续工作
      
    4.在计算机内存中,统一使用Unicode编码,当需要保存到硬盘或者需要传输的时候，就转换为UTF-8编码。
      例如:
            (1) 用记事本编辑的时候，从文件读取的UTF-8字符被转换为Unicode字符到内存里,编辑完成后,
                保存的时候再把Unicode转换为UTF-8保存到文件
                
            (2) 浏览网页的时候，服务器会把动态生成的Unicode内容转换为UTF-8再传输到浏览器,所以你看到很多网页的
                源码上会有类似<meta charset="UTF-8" />的信息，表示该网页正是用的UTF-8编码。
            
```  

### python 字符串

```shell

    A. 注意事项
        1. 在最新的Python 3版本中,字符串是以Unicode编码的,也就是说,Python的字符串支持多语言
                例如 >>> print('包含中文的str')
                    结果
                        包含中文的str
                        
        2.对于单个字符的编码,Python提供了ord()函数获取字符的整数表示,chr()函数把编码转换为对应的字符：
                例如
                    >>> ord('A')
                    65
                    >>> ord('中')
                    20013
                    
                    >>> chr(66)
                    'B'
                     >>> chr(25991)
                    '文'
         
        3.bytes类型的数据用带b前缀的单引号或双引号表示,在bytes中,优先显示ASCII字符,无法显示为ASCII字符的字节，用\x##显示。
        4.在操作字符串时，我们经常遇到str和bytes的互相转换。为了避免乱码问题，应当始终坚持使用UTF-8编码对str和bytes进行转换
        5.当你的源代码中包含中文的时候,在保存源代码时,就需要务必指定保存为UTF-8编码.当Python解释器读取源代码时,
          为了让它按UTF-8编码读取，我们通常在文件开头写上这两行：
                                                #!/usr/bin/env python3
                                                # -*- coding: utf-8 -*-
                                                
           第一行注释是为了告诉Linux/OS X系统，这是一个Python可执行程序，Windows系统会忽略这个注释；
           第二行注释是为了告诉Python解释器，按照UTF-8编码读取源代码，否则，你在源代码中写的中文输出可能会有乱码
           
        6.申明了UTF-8编码并不意味着你的.py文件就是UTF-8编码的，必须并且要确保文本编辑器正在使用UTF-8 without BOM编码
        7.字符串格式化输出
            (1) >>> 'Hi, %s, you have $%d.' % ('Michael', 1000000)    (其中与C语言不同, 用"%" 代替了 ",")
                'Hi, Michael, you have $1000000.'
                
            (2) 字符串里面的%是一个普通字符怎么办？这个时候就需要转义，用%%来表示一个%
                    >>> 'growth rate: %d %%' % 7
                    'growth rate: 7 %'
                    
        8
        
    B 函数
    
        1.encode()方法
            编码为指定的bytes用于网络的传输
            
            >>> 'ABC'.encode('ascii')
            b'ABC'
            
            >>> '中文'.encode('utf-8')
            b'\xe4\xb8\xad\xe6\x96\x87'
            
            >>> '中文'.encode('ascii')
            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
            UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
            含有中文的str无法用ASCII编码，因为中文编码的范围超过了ASCII编码的范围，Python会报错
            
        2.decode()
            解码为str字符串
                >>> b'ABC'.decode('ascii')
                'ABC'
                
               (1) 如果bytes中包含无法解码的字节，decode()方法会报错
               
                        >>> b'\xe4\xb8\xad\xff'.decode('utf-8')
                        Traceback (most recent call last):
                          ...
                        UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 3: invalid start byte
                        
               (2) 如果bytes中只有一小部分无效的字节，可以传入errors='ignore'忽略错误的字节
               
                        >>> b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore')
                        '中'
                        
        3.len()函数
            (1) 如果传入的参数为str,则计算str有多少个字符
                    >>> len('ABC')
                    3
                    >>> len('中文')
                    2
            (2) 如果传入的参数为byte,则计算有多少个字节数
                    >>> len(b'\xe4\xb8\xad\xe6\x96\x87')
                    6
                    >>> len('中文'.encode('utf-8'))
                    6
                    
        4.int()函数 :将str转化为int
            int int(str),
            
        5.str.replace() 函数
                对于不可变对象，比如str,
                    >>> a = 'abc'
                    >>> a.replace('a', 'A')
                    'Abc'
                    >>> a
                    'abc'
        
```  

### 复杂数据结构

#### list
 
```shell
    1. list 定义
            >>> 变量名=['list1','list2']
   2.获取最后一个元素
            >>> list[-1]
            
   3.list.append(value): 向队尾加入新的元素
   4.list.insert(index,value)
        向第index位置插入value,剩下的顺位后移
        
        >>> classmates
        ['Michael', 'Bob', 'Tracy', 'Adam']
        >>> classmates.insert(1, 'Jack')
        >>> classmates
        ['Michael', 'Jack', 'Bob', 'Tracy', 'Adam']
        
   5.list.pop() :删除list队为元素
   6.list.pop(index) :删除指定位置的元素
   7.把某个元素替换成别的元素,可以直接赋值给对应的索引位置
        >>> classmates[1] = 'Sarah'
        >>> classmates
        ['Michael', 'Sarah', 'Tracy']
        
   8.list里面的元素的数据类型也可以不同
        >>> L = ['Apple', 123, True]
        
   函数
        1.list.sort() 进行升序排序
            >>> a = ['c', 'b', 'a']
            >>> a.sort()
            >>> a
            ['a', 'b', 'c']
            
```  

#### tuple(元组)
  
```shell
    1. tuple一旦初始化就不能修改
    2.tuple定义
        >>> tuple_var = ('Michael', 'Bob', 'Tracy')
            
``` 

### 条件判断
  
```shell
    1. 
        age = 3
        if age >= 18:
            print('adult')
        elif age >= 6:
            print('teenager')
        else:
            print('kid')
            
``` 

### 循环
  
```shell
    1. for...in循环，依次把list或tuple中的每个元素迭代出来，
            names = ['Michael', 'Bob', 'Tracy']
            for name in names:
                print(name)
                
            
``` 

### dict
  
```shell
    1. dict的支持，dict全称dictionary，在其他语言中也称为map，使用键-值（key-value）存储，具有极快的查找速度
    2.
          >>> d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
          >>> d['Michael']
          95
          
    3.如果key不存在，dict就会报错
        >>> d['Thomas']
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        KeyError: 'Thomas'
        
    4.避免key不存在的错误
        (1) 通过in判断key是否存在
                >>> 'Thomas' in d
                False
        (2) 二是通过dict提供的get()方法,如果key不存在，可以返回None，或者自己指定的value：
                >>> d.get('Thomas')
                >>> d.get('Thomas', -1)
                -1
                
    5.删除一个key dict.pop(key)
        >>> d.pop('Bob')
        75
        >>> d
        {'Michael': 95, 'Tracy': 85}
        
    6.注意:dict的key必须是不可变对象.这是因为dict根据key来计算value的存储位置,如果每次计算相同的key得出的结果不同,
           那dict内部就完全混乱了。这个通过key计算位置的算法称为哈希算法（Hash）。
           要保证hash的正确性，作为key的对象就不能变。在Python中，字符串、整数等都是不可变的，因此,
           可以放心地作为key。而list是可变的，就不能作为key：
                  
``` 

### set

```shell
    1. set和dict类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key
    2.set可以看成数学意义上的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集、并集等操作
            >>> s1 = set([1, 2, 3])
            >>> s2 = set([2, 3, 4])
            >>> s1 & s2
            {2, 3}
            >>> s1 | s2
            {1, 2, 3, 4}
                  
``` 

### 函数

```shell
    1. 定义函数
        定义一个函数要使用def语句，依次写出函数名、括号、括号中的参数和冒号:
        
        #! /usr/bin/env python3
        # -*- coding: utf-8 -*-
        def my_abs(x):
            if x >= 0:
                return x
            else:
                return -x
                
    2.在Python交互环境中定义函数时，注意Python会出现...的提示。函数定义结束后需要按两次回车重新回到>>>提示符下
    3.如果你已经把my_abs()的函数定义保存为abstest.py文件了，那么，可以在该文件的当前目录下启动Python解释器，
      用 from abstest import my_abs 来导入my_abs()函数，注意abstest是文件名（不含.py扩展名）
      
    4.空函数:如果想定义一个什么事也不做的空函数，可以用pass语句,
        def 函数名():
            pass
            
    5.返回多个值,返回值是一个tuple！但是，在语法上，返回一个tuple可以省略括号，而多个变量可以同时接收一个tuple,
      按位置赋给对应的值，所以，Python的函数返回多值其实就是返回一个tuple，但写起来更方便
        import math
        
        def move(x, y, step, angle=0):
            nx = x + step * math.cos(angle)
            ny = y - step * math.sin(angle)
            return nx, ny
            
            
    6.函数的参数
        (1) 默认参数
        
            A.示例
                def power(x, n=2):
                    s = 1
                    while n > 0:
                        n = n - 1
                        s = s * x
                    return s
                    
                >>> power(5)
                25
                >>> power(5, 2)
                25
            
            B 必选参数(显示输入)在前，默认参数在后，否则Python的解释器会报错
            C 
                def add_end(L=[]):
                    L.append('END')
                    return L
                    
                现象:
                    >>> add_end()
                    ['END']
                    >>> add_end()
                    ['END', 'END']
                    >>> add_end()
                    ['END', 'END', 'END']
                    
                原因:
                    Python函数在定义的时候,默认参数L的值就被计算出来了,即[],因为默认参数L也是一个变量,它指向对象[],
                    每次调用该函数，如果改变了L的内容，则下次调用时，默认参数的内容就变了，不再是函数定义时的[]了
                    
                    定义默认参数要牢记一点：默认参数必须指向不变对象！
                    
                修改例子:
                    def add_end(L=None):
                        if L is None:
                            L = []
                        L.append('END')
                        return L
                        
        (2) 可变参数
                A.可变参数就是传入的参数个数是可变的，可以是1个、2个到任意个，还可以是0个
                B.定义可变参数和定义一个list或tuple参数相比，仅仅在参数前面加了一个*号.
                  在函数内部，参数numbers接收到的是一个tuple，因此，函数代码完全不变。但是，调用该函数时，
                  可以传入任意个参数，包括0个参数
                  
                  示例代码:
                    def calc(*numbers):
                        sum = 0
                        for n in numbers:
                            sum = sum + n * n
                        return sum
                        
                    结果:
                        >>> calc(1, 2)
                        5
                        >>> calc()
                        0
                        
                C.如果已经有一个list或者tuple,在list或tuple前面加一个*号,把list或tuple的元素变成可变参数传进去
                    
                   示例代码:
                        >>> nums = [1, 2, 3]
                        >>> calc(*nums)
                        
                        结果:
                            14
                            
        (3) 关键字参数
                A.关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict
                    示例代码:
                        def person(name, age, **kw):
                            print('name:', name, 'age:', age, 'other:', kw)
                            
                        也可以传入任意个数的关键字参数:
                            >>> person('Bob', 35, city='Beijing')
                            name: Bob age: 35 other: {'city': 'Beijing'}
                            >>> person('Adam', 45, gender='M', job='Engineer')
                            name: Adam age: 45 other: {'gender': 'M', 'job': 'Engineer'}
                            
                B.可以扩展函数的功能。比如,在person函数里,我们保证能接收到name和age这两个参数,但是,
                  如果调用者愿意提供更多的参数，我们也能收到。试想你正在做一个用户注册的功能，除了用户名和年龄是必填项外，
                  其他都是可选项，利用关键字参数来定义这个函数就能满足注册的需求
                  
                C.可以先组装出一个dict，然后，把该dict转换为关键字参数传进去
                       >>> extra = {'city': 'Beijing', 'job': 'Engineer'}
                       >>> person('Jack', 24, **extra)
                       name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}
                       
                   **extra表示把extra这个dict的所有key-value用关键字参数传入到函数的**kw参数，kw将获得一个dict，
                   注意:
                        kw获得的dict是extra的一份拷贝，对kw的改动不会影响到函数外的extra
                        
                D.命名关键字参数
                    1.对于关键字参数，函数的调用者可以传入任意不受限制的关键字参数,而命名关键字参数则可以限制关键字参数的名字,
                      和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数.
                       例如，只接收city和job作为关键字参数
                            def person(name, age, *, city, job):
                                print(name, age, city, job)
                                
                            >>> person('Jack', 24, city='Beijing', job='Engineer')
                            Jack 24 Beijing Engineer
                            
                    2.如果函数定义中已经有了一个可变参数，后面跟着的命名关键字参数就不再需要一个特殊分隔符*了
                        def person(name, age, *args, city, job):
                            print(name, age, args, city, job)
                            
                    3.命名关键字参数必须传入参数名，这和位置参数不同。如果没有传入参数名，调用将报错：
                        错误用法:
                            >>> person('Jack', 24, 'Beijing', 'Engineer')
                            Traceback (most recent call last):
                              File "<stdin>", line 1, in <module>
                            TypeError: person() takes 2 positional arguments but 4 were given
                            
                            由于调用时缺少参数名city和job，Python解释器把这4个参数均视为位置参数，
                            但person()函数仅接受2个位置参数。
                            
                        正确用法:
                            >>> person('Jack', 24, 'city':'Beijing', 'job':'Engineer')
                            
                    4.使用命名关键字参数时,如果没有可变参数,就必须加一个*作为特殊分隔符。
                      如果缺少*,Python解释器将无法识别位置参数和命名关键字参数
                      
        (4) 参数组合
                A. 参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数。
                
        (5) *args是可变参数，args接收的是一个tuple；
            **kw是关键字参数，kw接收的是一个dict。
            使用*args和**kw是Python的习惯写法，当然也可以用其他参数名，但最好使用习惯用法
            
    7.递归函数
        (1) 递归调用栈溢出的方法是通过尾递归优化,尾递归是指，在函数返回的时候，调用自身本身，并且，
            return语句不能包含表达式。这样，编译器或者解释器就可以把尾递归做优化，使递归本身无论调用多少次，
            都只占用一个栈帧，不会出现栈溢出的情况
            
            def fact(n):
                return fact_iter(n, 1)
            
            def fact_iter(num, product):
                if num == 1:
                    return product
                return fact_iter(num - 1, num * product)
                
        (2) 遗憾的是，大多数编程语言没有针对尾递归做优化，Python解释器也没有做优化，所以，
             即使把上面的fact(n)函数改成尾递归方式，也会导致栈溢出
                              
``` 

### 高级特性

#### 切片

```shell
    切片(Slice) L[start_index:get_num] 或则是
       L[start_index:get_num:skip_num](其中skip_num为在start_index~get_num+start_index范围内隔skip_num取一个)
       
        A.取前3个元素，用一行代码就可以完成切片
            >>> L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
            >>> L[0:3]
                ['Michael', 'Sarah', 'Tracy']
                
        B.如果第一个索引是0，还可以省略
            >>> L[:3]
            ['Michael', 'Sarah', 'Tracy']
            
        C.支持倒数切片,倒数第一个元素的索引是-1
            >>> L[-2:]
            ['Bob', 'Jack']
            
        D.范围在前10个数，每两个取一个
            >>> L
            [0, 1, 2, 3, ..., 99]
            >>> L[:10:2]
            [0, 2, 4, 6, 8]
            
        E.所有数，每5个取一个
            >>> L[::5]
            [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
            
        F.只写[:]就可以原样复制一个list：
            >>> L[:]
            [0, 1, 2, 3, ..., 99]
            
        G.字符串'xxx'也可以看成是一种list，每个元素就是一个字符。
          因此，字符串也可以用切片操作，只是操作结果仍是字符串：
            >>> 'ABCDEFG'[:3]
            'ABC'
            >>> 'ABCDEFG'[::2]
            'ACEG'             
``` 

#### 迭代

```shell
    1.迭代是通过for ... in来完成的, 不仅可以用在list或tuple上，还可以作用在其他可迭代对象上
      list这种数据类型虽然有下标,但很多其他数据类型是没有下标的，但是，只要是可迭代对象，无论有无下标，都可以迭代,
        A.
          比如dict就可以迭代：
                >>> d = {'a': 1, 'b': 2, 'c': 3}
                >>> for key in d:
                ...     print(key)
                ...
                结果
                a
                c
                b
                
        B.默认情况下,dict迭代的是key.如果要迭代value,可以用for value in d.values(),
          如果要同时迭代key和value,可以用for k, v in d.items()
          
    2.通过collections模块的Iterable类型判断
        >>> from collections import Iterable
        >>> isinstance('abc', Iterable) # str是否可迭代
        True
        >>> isinstance([1,2,3], Iterable) # list是否可迭代
        True
        >>> isinstance(123, Iterable) # 整数是否可迭代
        False
        
    3.内置的enumerate函数可以把一个list变成 索引-元素 对,这样就可以在for循环中同时迭代索引和元素本身
            >>> for i, value in enumerate(['A', 'B', 'C']):
            ...     print(i, value)
            ...
            0 A
            1 B
            2 C
            
    4.在for循环里，同时引用了两个变量，在Python里是很常见的
            >>> for x, y in [(1, 1), (2, 4), (3, 9)]:
            ...     print(x, y)
            ...
            1 1
            2 4
            3 9
``` 

#### 迭代器

```shell
    1.可以直接作用于for循环的对象统称为可迭代对象：Iterable,
       可以使用isinstance()判断一个对象是否是Iterable对象
                    >>> from collections import Iterable
                    >>> isinstance('abc', Iterable) # str是否可迭代
                    True
                    >>> isinstance((x for x in range(10)), Iterable)
                    True
    2.可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator
      可以使用isinstance()判断一个对象是否是Iterator对象
          >>> from collections import Iterator
          >>> isinstance((x for x in range(10)), Iterator)
          True
          >>> isinstance([], Iterator)
          False
          >>> isinstance({}, Iterator)
          False
          >>> isinstance('abc', Iterator)
          False
          
    3.生成器都是Iterator对象,但list、dict、str虽然是Iterable，却不是Iterator,Iterator对象表示的是一个数据流,
      Iterator对象可以被next()函数调用并不断返回下一个数据,直到没有数据时抛出StopIteration错误。
      可以把这个数据流看做是一个有序序列，但我们却不能提前知道序列的长度，只能不断通过next()函数实现按需计算下一个数据，
      所以Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算。 Iterator甚至可以表示一个无限大的数据流，
      例如全体自然数。而使用list是永远不可能存储全体自然数的。
      
      把list、dict、str等Iterable变成Iterator可以使用iter()函数
            >>> isinstance(iter([]), Iterator)
            True
            >>> isinstance(iter('abc'), Iterator)
            True
      
``` 

#### 列表生成式

```shell
    1.列表生成式即List Comprehensions,可以用来创建list的生成式
        要生成[1x1, 2x2, 3x3, ..., 10x10]:
            >>> [x * x for x in range(1, 11)]
            [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
            
    2.for循环后面还可以加上if判断
        >>> [x * x for x in range(1, 11) if x % 2 == 0]
        [4, 16, 36, 64, 100]
        
    3.使用两层循环，可以生成全排列
        >>> [m + n for m in 'ABC' for n in 'XYZ']
        ['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
        
    4.列表生成式也可以使用两个变量来生成list
        >>> d = {'x': 'A', 'y': 'B', 'z': 'C' }
        >>> [k + '=' + v for k, v in d.items()]
        ['y=B', 'x=A', 'z=C']
``` 

#### 生成器

```shell
    1.通过列表生成式,我们可以直接创建一个列表。但是,受到内存限制,列表容量肯定是有限的.而且，创建一个包含100万个元素的列表,
      不仅占用很大的存储空间，如果我们仅仅需要访问前面几个元素，那后面绝大多数元素占用的空间都白白浪费了。
      如果列表元素可以按照某种算法推算出来,那我们是否可以在循环的过程中不断推算出后续的元素呢？这样就不必创建完整的list,
      从而节省大量的空间在Python中,一边循环一边计算的机制，称为生成器：generator。
      
    2.创建一个generator,
        A.第一个方法 只要把一个列表生成式的[]改成()
            >>> g = (x * x for x in range(10))
            >>> g
            <generator object <genexpr> at 0x1022ef630>
           
        B.第二种方法 如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator
                def fib(max):
                    n, a, b = 0, 0, 1
                    while n < max:
                        yield b
                        a, b = b, a + b
                        n = n + 1
                    return 'done'
                    
                >>> f = fib(6)
                >>> f
                <generator object fib at 0x104feaaa0>
                
                >>> g = fib(6)
                >>> while True:
                ...     try:
                ...         x = next(g)
                ...         print('g:', x)
                ...     except StopIteration as e:
                ...         print('Generator return value:', e.value)
                ...         break
                ...
                g: 1
                g: 1
                g: 2
                g: 3
                g: 5
                g: 8
                Generator return value: done
                
                用for循环调用generator时，发现拿不到generator的return语句的返回值。如果想要拿到返回值,
                必须捕获StopIteration错误，返回值包含在StopIteration的value中
                
                注意:调用generator的函数，在每次调用next()的时候执行，遇到yield语句返回，
                    再次执行时从上次返回的yield语句处继续执行。
                    
                    例如:
                        def odd():
                            print('step 1')
                            yield 1
                            print('step 2')
                            yield(3)
                            print('step 3')
                            yield(5)
                            
                        >>> o = odd()
                        >>> next(o)
                        step 1
                        1
                        >>> next(o)
                        step 2
                        3
                        >>> next(o)
                        step 3
                        5
                        >>> next(o)
                        Traceback (most recent call last):
                          File "<stdin>", line 1, in <module>
                        StopIteration
        
    3.打印出generator的每一个元素,可以通过next()函数获得generator的下一个返回值(一般调试用)
        >>> next(g)
        0
        >>> next(g)
        1
        >>> next(g)
        4
        >>> next(g)
        9
        >>> next(g)
        16
        >>> next(g)
        25
        >>> next(g)
    4.正常情况下 使用for循环遍历每一个元素
        >>> g = (x * x for x in range(10))
        >>> for n in g:
        ...     print(n)
        ... 
        结果:
            0
            1
            4
            9
            1
``` 