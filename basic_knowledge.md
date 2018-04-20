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