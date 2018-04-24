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