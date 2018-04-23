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