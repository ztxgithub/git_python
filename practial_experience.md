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

## 错误处理
 
```shell

    1.
     try:
          print('try...')
          r = 10 / 0
          print('result:', r)
      except ZeroDivisionError as e:
          print('except:', e)
      finally:
          print('finally...')
      print('END')
      
     (1) 如果try代码中发生错误,则会直接跳到 except语句块中
     (2) finally 不管有没有发送错误都执行 finally的代码
     (3) 如果没有错误发生，可以在except语句块后面加一个else，当没有错误发生时，会自动执行else语句
     
    2.使用try...except捕获错误还有一个巨大的好处，就是可以跨越多层调用，比如函数main()调用foo()，foo()调用bar()，
      结果bar()出错了，这时，只要main()捕获到了，就可以处理,不需要在每个可能出错的地方去捕获错误，
      只要在合适的层次去捕获错误就可以了。这样一来，就大大减少了写try...except...finally的麻烦
          def foo(s):
              return 10 / int(s)
          
          def bar(s):
              return foo(s) * 2
          
          def main():
              try:
                  bar('0')
              except Exception as e:
                  print('Error:', e)
              finally:
                  print('finally...')
                  
    3.记录错误
        Python内置的logging模块可以非常容易地记录错误信息
            # err_logging.py
            
            import logging
            
            def foo(s):
                return 10 / int(s)
            
            def bar(s):
                return foo(s) * 2
            
            def main():
                try:
                    bar('0')
                except Exception as e:
                    logging.exception(e)
            
            main()
            print('END')
            
    4.常见的问题处理
        # err_reraise.py
        
        def foo(s):
            n = int(s)
            if n==0:
                raise ValueError('invalid value: %s' % s)
            return 10 / n
        
        def bar():
            try:
                foo('0')
            except ValueError as e:
                print('ValueError!')
                raise
        
        bar()
        
      捕获错误目的只是记录一下，便于后续追踪。但是，由于当前函数不知道应该怎么处理该错误，所以，
      最恰当的方式是继续往上抛，让顶层调用者去处理.
      
      raise语句如果不带参数，就会把当前错误原样抛出。此外，在except中raise一个Error，还可以把一种类型的错误转化成另一种类型：
            try:
                10 / 0
            except ZeroDivisionError:
                raise ValueError('input error!')
     
```