# python 函数式编程
 
## pyhton 简介

```shell

    1.函数式编程就是一种抽象程度很高的编程范式,纯粹的函数式编程语言编写的函数没有变量，因此，任意一个函数，
     只要输入是确定的，输出就是确定的，这种纯函数我们称之为没有副作用。
     而允许使用变量的程序设计语言，由于函数内部的变量状态不确定，同样的输入，可能得到不同的输出，因此，这种函数是有副作用的.
     
    2.函数式编程的一个特点就是,允许把函数本身作为参数传入另一个函数，还允许返回一个函数
    
    3.Python对函数式编程提供部分支持。由于Python允许使用变量，因此，Python不是纯函数式编程语言

```

## 高阶函数

### map()函数

```shell

    1.map()函数接收两个参数,一个是函数,一个是Iterable,map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回
        >>> def f(x):
        ...     return x * x
        ...
        >>> r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> list(r)
        [1, 4, 9, 16, 25, 36, 49, 64, 81]
        
    2.map()作为高阶函数,事实上它把运算规则抽象了,因此，我们不但可以计算简单的f(x)=x2，还可以计算任意复杂的函数，
      比如，把这个list所有数字转为字符串
            >>> list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
            ['1', '2', '3', '4', '5', '6', '7', '8', '9']

```

### reduce()函数

```shell

    1.reduce把一个函数fun作用在一个序列[x1, x2, x3, ...]上,fun这个函数必须接收两个参数,
      reduce把 函数结果继续和序列的下一个元素
      做累积计算，其效果就是：
            reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
            
    2.对一个序列求和,就可以用reduce实现：
            >>> from functools import reduce
            >>> def add(x, y):
            ...     return x + y
            ...
            >>> reduce(add, [1, 3, 5, 7, 9])
            25
            
```

### filter()函数

```shell

    1.用于过滤序列,把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素
            例如，在一个list中，删掉偶数，只保留奇数:
                def is_odd(n):
                    return n % 2 == 1
                
                list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
                
    2.注意 filter()函数返回的是一个Iterator，也就是一个惰性序列，所以要强迫filter()完成计算结果,
      需要用list()函数获得所有结果并返回list。
            
```

### sorted()排序算法

```shell

    1.可以接收一个key函数来实现自定义的排序，例如按绝对值大小排序：
        >>> sorted([36, 5, -12, 9, -21], key=abs)
        [5, 9, -12, -21, 36]
    2.忽略大小写进行字符串排序
        >>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)
        ['about', 'bob', 'Credit', 'Zoo']
        
    3.进行反向排序，不必改动key函数，可以传入第三个参数reverse=True：
        >>> sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
        ['Zoo', 'Credit', 'bob', 'about']
            
```

## 返回函数

```shell

    1.函数作为返回值
        定义一个求和函数,如果不需要立刻求和，而是在后面的代码中，根据需要再计算,可以不返回求和的结果，而是返回求和的函数
        def lazy_sum(*args):
            def sum():
                ax = 0
                for n in args:
                    ax = ax + n
                return ax
            return sum
            
        当我们调用lazy_sum()时，返回的并不是求和结果，而是求和函数：
        >>> f = lazy_sum(1, 3, 5, 7, 9)
        >>> f
        <function lazy_sum.<locals>.sum at 0x101c6ed90>
        >>> f()
        25
        
        在这个例子中,我们在函数lazy_sum中又定义了函数sum，并且，内部函数sum可以引用外部函数lazy_sum的参数和局部变量，
        当lazy_sum返回函数sum时，相关参数和变量都保存在返回的函数中，这种称为“闭包（Closure）”的程序结构拥有极大的威力
        
            
    2.闭包
        A.返回函数不要引用任何循环变量，或者后续会发生变化的变量
            
```

## 匿名函数

```shell

    1.当我们在传入函数时,有些时候，不需要显式地定义函数，直接传入匿名函数更方便
    2. 匿名函数lambda x: x * x, 关键字lambda表示匿名函数，冒号(:)前面的x表示函数参数,匿名函数有个限制,
       就是只能有一个表达式,而且不用写return，返回值就是该表达式的结果
       
    3.用匿名函数有个好处,因为函数没有名字，不必担心函数名冲突。此外，匿名函数也是一个函数对象,
      也可以把匿名函数赋值给一个变量，再利用变量来调用该函数：
            >>> f = lambda x: x * x
            >>> f
            <function <lambda> at 0x101c6ef28>
            >>> f(5)
            25
            
    4.Python对匿名函数的支持有限，只有一些简单的情况下可以使用匿名函数。
           
```

## 装饰器

```shell

    1.函数对象有一个__name__属性，可以拿到函数的名字：
        >>> def now():
        ...     print('2015-3-25')
        ...
        >>> f = now
        >>> f.__name__
        结果:
        'now'
        
    2.假设我们要增强now()函数的功能，比如，在函数调用前后自动打印日志，但又不希望修改now()函数的静态代码实现,
      这种只在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator）
      
    3.本质上，decorator就是一个返回函数的高阶函数
    
        def log(func):
            def wrapper(*args, **kw):
                print('call %s():' % func.__name__)
                return func(*args, **kw)
            return wrapper
            
        借助Python的@语法，把decorator置于函数的定义处：
        @log
        def now():
            print('2015-3-25')
            
            
        把@log放到now()函数的定义处，相当于执行了语句：
            now = log(now)  其中now是一个函数变量
            
        但是
            >>> now.__name__
            'wrapper'
            
        因为返回的那个wrapper()函数名字就是'wrapper'，所以，需要把原始函数的__name__等属性复制到wrapper()函数中，
        否则，有些依赖函数签名的代码执行就会出错。
        
        完整的代码:
            import functools
            
            def log(func):
                @functools.wraps(func)
                def wrapper(*args, **kw):
                    print('call %s():' % func.__name__)
                    return func(*args, **kw)
                return wrapper
           
```

## 偏函数

```shell

    1.Python的functools模块提供了很多有用的功能,其中一个就是偏函数（Partial function）
    2.int()函数可以把字符串转换为整数，当仅传入字符串时，int()函数默认按十进制转换,
      int()函数还提供额外的base参数，默认值为10。如果传入base参数，就可以做N进制的转换：
        >>> int('12345', base=8)
        5349
        >>> int('12345', 16)
        74565
        
      假设要转换大量的二进制字符串,每次都传入int(x, base=2)非常麻烦，于是，我们想到，
      可以定义一个int2()的函数，默认把base=2传进去：
            def int2(x, base=2):
                return int(x, base)
                
            >>> int2('1000000')
            64
            
      functools.partial就是帮助我们创建一个偏函数的,不需要我们自己定义int2()，
      可以直接使用下面的代码创建一个新的函数int2：
            >>> import functools
            >>> int2 = functools.partial(int, base=2)
            >>> int2('1000000')
            64
            >>> int2('1010101')
            85
            
      创建偏函数时，实际上可以接收函数对象、*args和**kw这3个参数，
        当传入：
            int2 = functools.partial(int, base=2)
        实际上固定了int()函数的关键字参数base，也就是：
            int2('10010') 相当于： kw = { 'base': 2 } int('10010', **kw)
            
        当传入:
            max2 = functools.partial(max, 10)
        实际上会把10作为*args的一部分自动加到左边，也就是：
            max2(5, 6, 7) 相当于： args = (10, 5, 6, 7) max(*args)
            结果为 10
            
            
    3.functools.partial的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），
      返回一个新的函数，调用这个新函数会更简单
           
```