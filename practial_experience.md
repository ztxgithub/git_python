# python 技巧
 
```shell

    1.类似__xxx__的属性和方法在Python中都是有特殊用途的,比如__len__方法返回长度。在Python中,
      如果你调用len()函数试图获取一个对象的长度，实际上，在len()函数内部，它自动去调用该对象的__len__()方法,
      下面的代码是等价的：
      
      >>> len('ABC')
      3
      >>> 'ABC'.__len__()
      3
      
    2.我们自己写的类，如果也想用len(myObj)的话，就自己写一个__len__()方法：
        >>> class MyDog(object):
        ...     def __len__(self):
        ...         return 100
        ...
        >>> dog = MyDog()
        >>> len(dog)
        100
```