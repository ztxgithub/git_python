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

## 调试

```shell

    1.断言 assert
        def foo(s):
            n = int(s)
            assert n != 0, 'n is zero!'
            return 10 / n
        
        def main():
            foo('0')
            
      表达式n != 0应该是True，否则，根据程序运行的逻辑，后面的代码肯定会出错
      启动Python解释器时可以用-O参数来关闭assert：
        $ python -O err.py
        Traceback (most recent call last):
          ...
        ZeroDivisionError: division by zero
        
    2.logging
        它允许你指定记录信息的级别，有debug，info，warning，error等几个级别，当我们指定level=INFO时，logging.debug就不起作用了,
        logging的另一个好处是通过简单的配置，一条语句可以同时输出到不同的地方，比如console和文件
    
        import logging
        logging.basicConfig(level=logging.INFO)
        
        s = '0'
        n = int(s)
        logging.info('n = %d' % n)
        print(10 / n)
        
    3.pdb
        1.$ python -m pdb err.py
          > /Users/michael/Github/learn-python3/samples/debug/err.py(2)<module>()
          -> s = '0'
          
        2.输入命令 l 来查看代码
        3.输入命令 n 可以单步执行代码
        4.输入命令 "p 变量名" 来查看变量
        5.输入 命令q 结束调试
        6.命令c继续运行
        
    4.pdb.set_trace()
        这个方法也是用pdb，但是不需要单步执行，我们只需要import pdb，然后，
        在可能出错的地方放一个pdb.set_trace()，就可以设置一个断点
            # err.py
            import pdb
            
            s = '0'
            n = int(s)
            pdb.set_trace() # 运行到这里会自动暂停
            print(10 / n)
            
         运行代码，程序会自动在pdb.set_trace()暂停并进入pdb调试环境，可以用命令p查看变量，或者用命令c继续运行
         
    5.单元测试
        (A).测试驱动开发(TDD：Test-Driven Development)
        (B).单元测试是用来对一个模块、一个函数或者一个类来进行正确性检验的测试工作。如果单元测试通过,
          说明我们测试的这个函数能够正常工作.如果单元测试不通过，要么函数有bug，要么测试条件输入不正确，
          总之，需要修复使单元测试能够通过.如果我们对abs()函数代码做了修改,只需要再跑一遍单元测试，如果通过，
          说明我们的修改不会对abs()函数原有的行为造成影响，如果测试不通过，说明我们的修改与原有行为不一致，
          要么修改代码，要么修改测试。
          
            编写一个Dict类，这个类的行为和dict一致，但是可以通过属性来访问，用起来就像下面这样：
                >>> d = Dict(a=1, b=2)
                >>> d['a']
                1
                >>> d.a
                1
                
                mydict.py:
                class Dict(dict):
                
                    def __init__(self, **kw):
                        super().__init__(**kw)
                
                    def __getattr__(self, key):
                        try:
                            return self[key]
                        except KeyError:
                            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
                
                    def __setattr__(self, key, value):
                        self[key] = value
                        
            编写单元测试，我们需要引入Python自带的unittest模块，编写mydict_test.py如下
            以test开头的方法就是测试方法，不以test开头的方法不被认为是测试方法，测试的时候不会被执行,
                import unittest
                
                from mydict import Dict
                
                class TestDict(unittest.TestCase):
                
                    def test_init(self):
                        d = Dict(a=1, b='test')
                        self.assertEqual(d.a, 1)
                        self.assertEqual(d.b, 'test')
                        self.assertTrue(isinstance(d, dict))
                
                    def test_key(self):
                        d = Dict()
                        d['key'] = 'value'
                        self.assertEqual(d.key, 'value')
                
                    def test_attr(self):
                        d = Dict()
                        d.key = 'value'
                        self.assertTrue('key' in d)
                        self.assertEqual(d['key'], 'value')
                
                    def test_keyerror(self):
                        d = Dict()
                        with self.assertRaises(KeyError):
                            value = d['empty']
                
                    def test_attrerror(self):
                        d = Dict()
                        with self.assertRaises(AttributeError):
                            value = d.empty
                            
            (1) assertEqual()
                    self.assertEqual(abs(-1), 1) # 断言函数返回的结果与1相等
            (2) 重要的断言就是期待抛出指定类型的Error，比如通过d['empty']访问不存在的key时，断言会抛出KeyError
                    with self.assertRaises(KeyError):
                        value = d['empty']
                        
        (C).运行单元测试
            A,mydict_test.py的最后加上两行代码：
                if __name__ == '__main__':
                    unittest.main()
                    
              可以把mydict_test.py当做正常的python脚本运行：
              
              $ python mydict_test.py
              
            B.命令行通过参数-m unittest直接运行单元测试(推荐的做法)：
                $ python -m unittest mydict_test
                
        (D).setUp与tearDown
            你的测试需要启动一个数据库，这时，就可以在setUp()方法中连接数据库，在tearDown()方法中关闭数据库，这样，
            不必在每个测试方法中重复相同的代码
                class TestDict(unittest.TestCase):
                
                    def setUp(self):
                        print('setUp...')
                
                    def tearDown(self):
                        print('tearDown...')
                        
    6.文档测试
        1.自动执行写在注释中的这些代码
        
            # mydict2.py
            class Dict(dict):
                '''
                Simple dict but also support access as x.y style.
            
                >>> d1 = Dict()
                >>> d1['x'] = 100
                >>> d1.x
                100
                >>> d1.y = 200
                >>> d1['y']
                200
                >>> d2 = Dict(a=1, b=2, c='3')
                >>> d2.c
                '3'
                >>> d2['empty']
                Traceback (most recent call last):
                    ...
                KeyError: 'empty'
                >>> d2.empty
                Traceback (most recent call last):
                    ...
                AttributeError: 'Dict' object has no attribute 'empty'
                '''
                def __init__(self, **kw):
                    super(Dict, self).__init__(**kw)
            
                def __getattr__(self, key):
                    try:
                        return self[key]
                    except KeyError:
                        raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
            
                def __setattr__(self, key, value):
                    self[key] = value
            
            if __name__=='__main__':
                import doctest
                doctest.testmod()
                
            运行python mydict2.py:
                $ python mydict2.py
                
            注意:
                当编写的doctest运行都是正确时,不会输出任何信息,有错误才输出
                注意到最后3行代码。当模块正常导入时,doctest不会被执行。只有在命令行直接运行时，才执行doctest。
                所以，不必担心doctest会在非测试环境下执行。
```