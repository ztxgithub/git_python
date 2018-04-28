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
                    
    4.在python中,函数是对象,可以进行函数变量的赋值
    5.函数可以被定义在另一个函数里面
        def talk():
            # 你可以定义一个函数
            def whisper(word="yes"):
                return word.lower()+"..."
                
            .....
            
            return
    6.装饰器就是封装器,可以让你在 被装饰函数(自己编写函数) 之前或之后执行代码，而不必修改函数本身(自己编写函数)
    7.书写一个装饰器
        # 装饰器是一个以另一个函数为参数的函数
        def my_shiny_new_decorator(a_function_to_decorate):
        
           在这里，装饰器定义一个函数： 包装器.这个函数将原始函数进行包装，以达到在原始函数之前、之后执行代码的目的
            def the_wrapper_around_the_original_function():
        
                将你要在原始函数之前执行的代码放到这里
                print "Before the function runs"
        
                调用原始函数(需要带括号)
                a_function_to_decorate()
        
                将你要在原始函数之后执行的代码放到这里
                print "After the function runs"
        
            代码到这里，函数‘a_function_to_decorate’还没有被执行,我们将返回刚才创建的这个包装函数
            这个函数包含原始函数及要执行的附加代码，并且可以被使用
            return the_wrapper_around_the_original_function
            
        A.未使用装饰器语法:
        
            创建一个有效的函数
            def a_stand_alone_function():
                print "I am a stand alone function, don't you dare modify me"
            
            
            在这里你可以装饰这个函数，将函数传递给装饰器，装饰器将动态地将其包装在任何你想执行的代码中，然后返回一个新的函数
            a_stand_alone_function_decorated = my_shiny_new_decorator(a_stand_alone_function)
            
             调用新函数，可以看到装饰器的效果
            a_stand_alone_function_decorated()
            结果:
                Before the function runs
                I am a stand alone function, don't you dare modify me
                After the function runs
            
        B. 使用装饰器
                @my_shiny_new_decorator
                def another_stand_alone_function():
                    print "Leave me alone"
                    
                以上就等于 another_stand_alone_function = my_shiny_new_decorator(another_stand_alone_function)
                
                another_stand_alone_function()
                结果:
                Before the function runs
                Leave me alone
                After the function runs
                
    8.累加两个装饰器
        def bread(func):
            def wrapper():
                print "</''''''\>"
                func()
                print "<\______/>"
            return wrapper
        
        def ingredients(func):
            def wrapper():
                print "#tomatoes#"
                func()
                print "~salad~"
            return wrapper
        
        def sandwich(food="--ham--"):
            print food
        
        sandwich()
            结果:
            outputs: --ham--
        
        A.未使用装饰器语法:
            累加两个装饰器
            sandwich = bread(ingredients(sandwich))
            sandwich()
            结果:
                </''''''\>
                 #tomatoes#
                 --ham--
                 ~salad~
                <\______/>
                
        B,使用装饰器语法:
            装饰器位置的顺序很重要
            
            @bread
            @ingredients
            def sandwich(food="--ham--"):
                print food
            
            sandwich()
            结果:
                </''''''\>
                 #tomatoes#
                 --ham--
                 ~salad~
                <\______/>
                
    9.向装饰器函数传递参数
    
        装饰器函数
        def a_decorator_passing_arguments(function_to_decorate):
            def a_wrapper_accepting_arguments(arg1, arg2):
                    print "I got args! Look:", arg1, arg2
                    function_to_decorate(arg1, arg2)
            return a_wrapper_accepting_arguments
        
        当你调用装饰器返回的函数，实际上是调用包装函数，所以给包装函数传递参数即可将参数传给装饰器函数
        
        @a_decorator_passing_arguments
        def print_full_name(first_name, last_name):
            print "My name is", first_name, last_name
        
        print_full_name("Peter", "Venkman")
        结果:
            I got args! Look: Peter Venkman
            My name is Peter Venkman
            
    10.装饰方法(对应对象而言)
            Python中对象的方法和函数是一样的,除了对象的方法首个参数是指向当前对象的引用(self).
            这意味着你可以用同样的方法构建一个装饰器，只是必须考虑self
            
                def method_friendly_decorator(method_to_decorate):
                    def wrapper(self, lie):
                        lie = lie - 3 
                        return method_to_decorate(self, lie)
                    return wrapper
                
                class Lucy(object):
                
                    def __init__(self):
                        self.age = 32
                
                    @method_friendly_decorator
                    def sayYourAge(self, lie):
                        print "I am %s, what did you think?" % (self.age + lie)
                
                l = Lucy()
                l.sayYourAge(-3)
                #outputs: I am 26, what did you think?
                
                
    11.构造一个更加通用的装饰器,可以作用在任何函数或对象方法上，而不必关心其参数使用       
            def a_decorator_passing_arbitrary_arguments(function_to_decorate):
                包装函数可以接受任何参数
                def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):
                    print "Do I have args?:"
                    print args
                    print kwargs
                    function_to_decorate(*args, **kwargs)
                return a_wrapper_accepting_arbitrary_arguments
            
            @a_decorator_passing_arbitrary_arguments
            def function_with_no_argument():
                print "Python is cool, no argument here."
            
            function_with_no_argument()
            结果:
            Do I have args?:
            ()
            {}
            Python is cool, no argument here.
            
            传入可变参数
            @a_decorator_passing_arbitrary_arguments
            def function_with_arguments(a, b, c):
                print a, b, c
            
            function_with_arguments(1,2,3)
            结果:
            Do I have args?:
            (1, 2, 3)
            {}
            1 2 3
            
            传入关键字参数
            @a_decorator_passing_arbitrary_arguments
            def function_with_named_arguments(a, b, c, platypus="Why not ?"):
                print "Do %s, %s and %s like platypus? %s" %\
                (a, b, c, platypus)
            
            function_with_named_arguments("Bill", "Linus", "Steve", platypus="Indeed!")
            结果:
            Do I have args ? :
            ('Bill', 'Linus', 'Steve')
            {'platypus': 'Indeed!'}
            Do Bill, Linus and Steve like platypus? Indeed!
            
            class Mary(object):
                def __init__(self):
                    self.age = 31
            
                @a_decorator_passing_arbitrary_arguments
                def sayYourAge(self, lie=-3): # You can now add a default value
                    print "I am %s, what did you think ?" % (self.age + lie)
            
            m = Mary()
            m.sayYourAge()
            #outputs
            # Do I have args?:
            #(<__main__.Mary object at 0xb7d303ac>,)
            #{}
            #I am 28, what did you think?
            
    12.functools模块(得到的是原始的名称, 而不是封装器的名称)
        # 调试，打印函数的名字
        def foo():
            print "foo"
        
        print foo.__name__
        #outputs: foo
        
        # 但当你使用装饰器，这一切变得混乱
        def bar(func):
            def wrapper():
                print "bar"
                return func()
            return wrapper
        
        @bar
        def foo():
            print "foo"
        
        print foo.__name__
        #outputs: wrapper
        
        # "functools" 可以改变这点
        import functools
        
        def bar(func):
            # 我们所说的 "wrapper", 封装 "func"
            @functools.wraps(func)
            def wrapper():
                print "bar"
                return func()
            return wrapper
        
        @bar
        def foo():
            print "foo"
        
        # 得到的是原始的名称, 而不是封装器的名称
        print foo.__name__
        #outputs: foo
        
    13.装饰器的用途
            (1) 装饰器打印一个函数的执行时间
                    def benchmark(func):
                        """
                        装饰器打印一个函数的执行时间
                        """
                        import time
                        def wrapper(*args, **kwargs):
                            t = time.clock()
                            res = func(*args, **kwargs)
                            print func.__name__, time.clock()-t
                            return res
                        return wrapper
                        
             (2) 记录并打印一个函数的执行次数
                    def counter(func):
                        """
                        记录并打印一个函数的执行次数
                        """
                        def wrapper(*args, **kwargs):
                            wrapper.count = wrapper.count + 1
                            res = func(*args, **kwargs)
                            print "{0} has been used: {1}x".format(func.__name__, wrapper.count)
                            return res
                        wrapper.count = 0
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