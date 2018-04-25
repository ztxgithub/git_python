# python 面向对象编程
 
## pyhton 面向对象编程简介

```shell

    1.面向对象编程——Object Oriented Programming，简称OOP，是一种程序设计思想.OOP把对象作为程序的基本单元,
      一个对象包含了数据和操作数据的函数.
      而面向对象的程序设计把计算机程序视为一组对象的集合，而每个对象都可以接收其他对象发过来的消息，并处理这些消息，
      计算机程序的执行就是一系列消息在各个对象之间传递
      
    2.面向过程的程序设计把计算机程序视为一系列的命令集合，即一组函数的顺序执行。为了简化程序设计，
      面向过程把函数继续切分为子函数，即把大块函数通过切割成小块函数来降低系统的复杂度
      
    3.在Python中，所有数据类型都可以视为对象，当然也可以自定义对象。自定义的对象数据类型就是面向对象中的类（Class）的概念
    4.面向对象的设计思想是抽象出Class，根据Class创建Instance。
    5.类是创建实例的模板，而实例则是一个一个具体的对象，各个实例拥有的数据都互相独立，互不影响

```

## 面向对象相关编程技巧

```shell

    1.尝试给实例绑定一个方法,但是，给一个实例绑定的方法，对另一个实例是不起作用的
        >>> def set_age(self, age): # 定义一个函数作为实例方法
        ...     self.age = age
        ...
        >>> from types import MethodType
        >>> s.set_age = MethodType(set_age, s) # 给实例绑定一个方法
        >>> s.set_age(25) # 调用实例方法
        >>> s.age # 测试结果
        25
        
    2.为了给所有实例都绑定方法，可以给class绑定方法：
        >>> def set_score(self, score):
        ...     self.score = score
        ...
        >>> Student.set_score = set_score
        
    3.使用__slots__,限制实例的属性,只允许对Student实例添加name和age属性
        class Student(object):
            __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称
            
         >>> s = Student() # 创建新的实例
         >>> s.name = 'Michael' # 绑定属性'name'
         
         >>> s.score = 99 # 绑定属性'score'
         Traceback (most recent call last):
           File "<stdin>", line 1, in <module>
         AttributeError: 'Student' object has no attribute 'score'
         由于'score'没有被放到__slots__中，所以不能绑定score属性，试图绑定score将得到AttributeError的错误。
         
       注意:
            使用__slots__要注意，__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的
            
            >>> class GraduateStudent(Student):
            ...     pass
            ...
            >>> g = GraduateStudent()
            >>> g.score = 9999
            
    4.@property 装饰器负责把一个方法变成属性调用的(未来解决既能检查参数，又可以用类似属性这样简单的方式来访问类的变量)
    
            class Student(object):
            
                @property     (把一个getter方法变成属性，只需要加上@property就可以)
                def score(self):
                    return self._score
            
                @score.setter
                def score(self, value):
                    if not isinstance(value, int):
                        raise ValueError('score must be an integer!')
                    if value < 0 or value > 100:
                        raise ValueError('score must between 0 ~ 100!')
                    self._score = value
                    
                @property本身又创建了另一个装饰器@score.setter，负责把一个setter方法变成属性赋值
                
                    >>> s = Student()
                    >>> s.score = 60 # OK，实际转化为s.set_score(60)
                    >>> s.score # OK，实际转化为s.get_score()
                    60
                    >>> s.score = 9999
                    Traceback (most recent call last):
                      ...
                    ValueError: score must between 0 ~ 100!
                    
            (1) @property广泛应用在类的定义中，可以让调用者写出简短的代码，同时保证对参数进行必要的检查，
                这样，程序运行时就减少了出错的可能性
                
    5.__str__()
    
        >>> class Student(object):
        ...     def __init__(self, name):
        ...         self.name = name
        ...
        >>> print(Student('Michael'))
        <__main__.Student object at 0x109afb190>
        
        如果想要print打印好看,则只需要定义好__str__()方法，返回一个好看的字符串就可以了：
        
        >>> class Student(object):
        ...     def __init__(self, name):
        ...         self.name = name
        ...     def __str__(self):
        ...         return 'Student object (name: %s)' % self.name
        ...
        >>> print(Student('Michael'))
        Student object (name: Michael)
        
    6.__repr__()
        敲变量不用print，打印出来的实例还是不好看,直接显示变量调用的不是__str__()，而是__repr__(),
        两者的区别是__str__()返回用户看到的字符串,而__repr__()返回程序开发者看到的字符串，也就是说，__repr__()是为调试服务的
        >>> s = Student('Michael')
        >>> s
        <__main__.Student object at 0x109afb310>
        
        解决办法是再定义一个__repr__()。但是通常__str__()和__repr__()代码都是一样的:
        
        class Student(object):
            def __init__(self, name):
                self.name = name
            def __str__(self):
                return 'Student object (name=%s)' % self.name
            __repr__ = __str__
        

    7.__iter__()
        一个类想被用于for ... in循环，类似list或tuple那样,该方法返回一个迭代对象，然后,
        Python的for循环就会不断调用该迭代对象的__next__()方法拿到循环的下一个值，直到遇到StopIteration错误时退出循环.
        
        以斐波那契数列为例，写一个Fib类，可以作用于for循环
        class Fib(object):
            def __init__(self):
                self.a, self.b = 0, 1 # 初始化两个计数器a，b
        
            def __iter__(self):
                return self # 实例本身就是迭代对象，故返回自己
        
            def __next__(self):
                self.a, self.b = self.b, self.a + self.b # 计算下一个值
                if self.a > 100000: # 退出循环的条件
                    raise StopIteration()
                return self.a # 返回下一个值
                
        >>> for n in Fib():
        ...     print(n)
        ...
        1
        1
        2
        3
        5
        ...
        46368
        75025
        
    8.__getitem__()
        要表现得像list那样按照下标取出元素，需要实现__getitem__()方法
        
        class Fib(object):
            def __getitem__(self, n):
                a, b = 1, 1
                for x in range(n):
                    a, b = b, a + b
                return a
                
        >>> f = Fib()
        >>> f[0]
        1
        >>> f[1]
        1
        >>> f[2]
        2
        >>> f[3]
        3
        
    9.__getattr__()
        正常情况下，当我们调用类的方法或属性时，如果不存在，就会报错,要避免这个错误，除了可以加上一个score属性外,
        Python还有另一个机制，那就是写一个__getattr__()方法，动态返回一个属性
        
            class Student(object):
            
                def __init__(self):
                    self.name = 'Michael'
            
                def __getattr__(self, attr):
                    if attr=='score':
                        return 99
                        
        当调用不存在的属性时,比如score，Python解释器会试图调用__getattr__(self, 'score')来尝试获得属性，
        这样，我们就有机会返回score的值
            >>> s = Student()
            >>> s.name
            'Michael'
            >>> s.score
            99
            
        返回函数也是完全可以的
            class Student(object):
            
                def __getattr__(self, attr):
                    if attr=='age':
                        return lambda: 25
                        
        只是调用方式要变为：
            >>> s.age()
            25
            
        注意:
            只有在没有找到属性的情况下，才调用__getattr__，已有的属性，比如name，不会在__getattr__中查找。
            
        作用:
            可以针对完全动态的情况作调用
            
    10.__call__()
        一个对象实例可以有自己的属性和方法，当我们调用实例方法时，我们用instance.method()来调用,但我们定义一个__call__()方法,
        就可以直接对实例进行调用
            class Student(object):
                def __init__(self, name):
                    self.name = name
            
                def __call__(self):
                    print('My name is %s.' % self.name)
                    
            >>> s = Student('Michael')
            >>> s() # self参数不要传入
            My name is Michael.
            
        __call__()还可以定义参数,对实例进行直接调用就好比对一个函数进行调用一样，所以你完全可以把对象看成函数，
        把函数看成对象，因为这两者之间本来就没啥根本的区别
        
        我们需要判断一个对象是否能被调用,能被调用的对象就是一个Callable对象，比如函数和我们上面定义的带有__call__()的类实例
            >>> callable(Student())
            True
            >>> callable(max)
            True
            >>> callable([1, 2, 3])
            False
            >>> callable(None)
            False
            >>> callable('str')
            False
```

## 类和实例

```shell

    1. 定义类是通过class关键字：
            class Student(object):
                pass
                
       紧接着是(object),表示该类是从哪个类继承下来的，如果没有合适的继承类，就使用object类，这是所有类最终都会继承的类.
       
    2.类可以起到模板的作用,因此，可以在创建实例的时候，把一些我们认为必须绑定的属性强制填写进去。
      通过定义一个特殊的__init__方法，在创建实例的时候，就把name，score等属性绑上去：
      
            class Student(object):
            
                def __init__(self, name, score):
                    self.name = name
                    self.score = score
                    
      注意:
        特殊方法“__init__”前后分别有两个下划线,__init__方法的第一个参数永远是self,表示创建的实例本身.
        
    3.有了__init__方法，在创建实例的时候，就不能传入空的参数了，必须传入与__init__方法匹配的参数，
      但self不需要传，Python解释器自己会把实例变量传进去:
         >>> bart = Student('Bart Simpson', 59)
         >>> bart.name
         'Bart Simpson'
         
    4.和普通的函数相比，在类中定义的函数只有一点不同，就是第一个参数永远是实例变量self，并且，调用时，不用传递该参数
    
    5.和静态语言不同，Python允许对实例变量绑定任何数据，也就是说，对于两个实例变量，
      虽然它们都是同一个类的不同实例，但拥有的变量名称都可能不同
            >>> bart = Student('Bart Simpson', 59)
            >>> lisa = Student('Lisa Simpson', 87)
            >>> bart.age = 8
            >>> bart.age
            8
            >>> lisa.age
            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
            AttributeError: 'Student' object has no attribute 'age'

```

## 访问限制

```shell

    1. 让内部属性不被外部访问，可以把属性的名称前加上两个下划线__
            class Student(object):
            
                def __init__(self, name, score):
                    self.__name = name   (这里变量名如果以__开头，就变成了一个私有变量（private),只能内部访问)
                    self.__score = score
            
                def print_score(self):
                    print('%s: %s' % (self.__name, self.__score))

```

## 继承和多态

```shell

    1. “开闭”原则:调用方只管调用，不管细节，而当我们新增一种Animal的子类时，只要确保run()方法编写正确，不用管原来的代码是如何调用的.
    2.对于静态语言（例如Java和C语言）来说，如果需要传入Animal类型，则传入的对象必须是Animal类型或者它的子类，否则，将无法调用run()方法。
    3.对于Python这样的动态语言来说，则不一定需要传入Animal类型。我们只需要保证传入的对象有一个run()方法就可以,
      这就是动态语言的“鸭子类型”，它并不要求严格的继承体系，一个对象只要“看起来像鸭子，走起路来像鸭子”，那它就可以被看做是鸭子

```

## 获取对象信息

```shell
   1.使用type()
   2.使用isinstance() 总是优先使用isinstance()判断类型，可以将指定类型及其子类“一网打尽”。  
   3.使用dir()获得一个对象的所有属性和方法
   4.使用getattr()、setattr()以及hasattr()，我们可以直接操作一个对象的状态属性
   5.只有在不知道对象信息的时候，我们才会去获取对象信息。如果可以直接写 sum = obj.x + obj.y
     就不要写 sum = getattr(obj, 'x') + getattr(obj, 'y')
```

## 实例属性和类属性

```shell
   1.由于Python是动态语言，根据类创建的实例可以任意绑定属性,给实例绑定属性的方法是通过实例变量，或者通过self变量
        class Student(object):
            def __init__(self, name):
                self.name = name
        
        s = Student('Bob')
        s.score = 90
        
   2.如果Student类本身需要绑定一个属性呢？可以直接在class中定义属性，这种属性是类属性，归Student类所有
        class Student(object):
            name = 'Student'
            
   3.在编写程序的时候，千万不要对实例属性和类属性使用相同的名字，因为相同名称的实例属性将屏蔽掉类属性，
     但是当你删除实例属性后，再使用相同的名称，访问到的将是类属性。
        >>> s.name = 'Michael' # 给实例绑定name属性
        >>> print(s.name) # 由于实例属性优先级比类属性高，因此，它会屏蔽掉类的name属性
        Michael
        >>> print(Student.name) # 但是类属性并未消失，用Student.name仍然可以访问
        Student
        >>> del s.name # 如果删除实例的name属性
        >>> print(s.name) # 再次调用s.name，由于实例的name属性没有找到，类的name属性就显示出来了
        Student
```

## 多重继承

```shell
   1.
        class Dog(Mammal, Runnable):
            pass
            
   2.Mixln
        在设计类的继承关系时，通常，主线都是单一继承下来的，例如，Ostrich继承自Bird。但是，如果需要“混入”额外的功能，
        通过多重继承就可以实现，比如，让Ostrich除了继承自Bird外，再同时继承Runnable。这种设计通常称之为MixIn。
        
        为了更好地看出继承关系，我们把Runnable和Flyable改为RunnableMixIn和FlyableMixIn。
        类似的，你还可以定义出肉食动物CarnivorousMixIn和植食动物HerbivoresMixIn，让某个动物同时拥有好几个MixIn
        
        class Dog(Mammal, RunnableMixIn, CarnivorousMixIn):
            pass
            
        MixIn的目的就是给一个类增加多个功能，这样，在设计类的时候，我们优先考虑通过多重继承来组合多个MixIn的功能，
        而不是设计多层次的复杂的继承关系
```

## 枚举类

```shell
   1.Enum类
        from enum import Enum
        
        Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
        其中 等号左边的Month 与 Enum第一个参数的名字要一致
        可以直接使用Month.Jan来引用一个常量，或者枚举它的所有成员：
            for name, member in Month.__members__.items():
                print(name, '=>', member, ',', member.value)
                
            value属性则是自动赋给成员的int常量，默认从1开始计数
            
        如果需要更精确地控制枚举类型，可以从Enum派生出自定义类:
            from enum import Enum, unique
            
            @unique      ## @unique装饰器可以帮助我们检查保证没有重复值。
            class Weekday(Enum):
                Sun = 0 # Sun的value被设定为0
                Mon = 1
                Tue = 2
                Wed = 3
                Thu = 4
                Fri = 5
                Sat = 6
                
            >>> day1 = Weekday.Mon
            >>> print(day1)
            Weekday.Mon
            >>> print(Weekday.Tue)
            Weekday.Tue
            >>> print(Weekday['Tue'])
            Weekday.Tue
            >>> print(Weekday.Tue.value)
            2
            >>> print(Weekday(1))
            Weekday.Mon
            >>> print(day1 == Weekday(1))
            True
            >>> Weekday(7)
            Traceback (most recent call last):
              ...
            ValueError: 7 is not a valid Weekday
```

## 元类

```shell
   1.动态语言和静态语言最大的不同,就是函数和类的定义，不是编译时定义的，而是运行时动态创建的。
   2.metaclass(元类)
        当我们定义了类以后，就可以根据这个类创建出实例，所以：先定义类，然后创建实例,
        如果我们想创建出类呢？那就必须根据metaclass创建出类，所以：先定义metaclass，然后创建类。
        先定义metaclass，就可以创建类，最后创建实例
        可以把类看成是metaclass创建出来的“实例”。
```