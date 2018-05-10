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

## 操作文件和目录

```shell
    1.获取详细的系统信息
        (1) >>> import os
        (2) >>> os.uname()
        
    2.获取环境变量
        >>> os.environ
        
    3.获取某个环境变量的值,可以调用os.environ.get('key')
            >>> os.environ.get('PATH')
            '/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/X11/bin:/usr/local/mysql/bin'
            >>> os.environ.get('x', 'default')
            'default'
            
    4.操作文件和目录的函数一部分放在os模块中，一部分放在os.path模块中，这一点要注意一下。
            查看、创建和删除目录可以这么调用：
                # 查看当前目录的绝对路径:
                >>> os.path.abspath('.')
                '/Users/michael'
                # 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来:
                >>> os.path.join('/Users/michael', 'testdir')
                '/Users/michael/testdir'
                # 然后创建一个目录:
                >>> os.mkdir('/Users/michael/testdir')
                # 删掉一个目录:
                >>> os.rmdir('/Users/michael/testdir')
                
    4.os.path.join()函数
        把两个路径合成一个时，不要直接拼字符串,可以正确处理不同操作系统的路径分隔符
        
    5.os.path.split()函数 拆分路径
        要拆分路径时，也不要直接去拆字符串，而要通过os.path.split()函数，
        这样可以把一个路径拆分为两部分，后一部分总是最后级别的目录或文件名：
            >>> os.path.split('/Users/michael/testdir/file.txt')
            ('/Users/michael/testdir', 'file.txt')
            
    6.os.path.splitext() 得到文件扩展名
        >>> os.path.splitext('/path/to/file.txt')
        ('/path/to/file', '.txt')
        
    7.复制文件的函数居然在os模块中不存在,
      shutil模块提供了copyfile()的函数，你还可以在shutil模块中找到很多实用函数，它们可以看做是os模块的补充
      
    8.列出当前目录下的所有目录
        >>> [x for x in os.listdir('.') if os.path.isdir(x)]
        ['.lein', '.local', '.m2', '.npm', '.ssh', '.Trash', '.vim', 'Applications', 'Desktop', ...]
    9.列出所有的.py文件
        >>> [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
        ['apis.py', 'config.py', 'models.py', 'pymonitor.py', 'test_db.py', 'urls.py', 'wsgiapp.py']
        
```

## 进程和线程

```shell
    1.Python的os模块封装了常见的系统调用，其中就包括fork，可以在Python程序中轻松创建子进程：
        import os
        
        print('Process (%s) start...' % os.getpid())
        # Only works on Unix/Linux/Mac:
        pid = os.fork()
        if pid == 0:
            print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
        else:
            print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
            
    2.multiprocessing
        (1) multiprocessing模块就是跨平台版本(linux/windows)的多进程模块
            multiprocessing模块提供了一个Process类来代表一个进程对象
            
                    from multiprocessing import Process
                    import os
                    
                    # 子进程要执行的代码
                    def run_proc(name):
                        print('Run child process %s (%s)...' % (name, os.getpid()))
                    
                    if __name__=='__main__':
                        print('Parent process %s.' % os.getpid())
                        p = Process(target=run_proc, args=('test',))
                        print('Child process will start.')
                        p.start()
                        p.join()
                        print('Child process end.')
                        
                        
                    结果:
                        Parent process 110240.
                        Child process will start.
                        Run child process test (110241)...
                        Child process end.
                        
    3.Pool
        (1) 启动大量的子进程，可以用进程池的方式批量创建子进程
                from multiprocessing import Pool
                import os, time, random
                
                def long_time_task(name):
                    print('Run task %s (%s)...' % (name, os.getpid()))
                    start = time.time()
                    time.sleep(random.random() * 3)
                    end = time.time()
                    print('Task %s runs %0.2f seconds.' % (name, (end - start)))
                
                if __name__=='__main__':
                    print('Parent process %s.' % os.getpid())
                    p = Pool(4)
                    for i in range(5):
                        p.apply_async(long_time_task, args=(i,))
                    print('Waiting for all subprocesses done...')
                    p.close()
                    p.join()
                    print('All subprocesses done.')
                    
                对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()，
                调用close()之后就不能继续添加新的Process了
                
    4.子进程
        (1) subprocess模块可以让我们非常方便地启动一个子进程，然后控制其输入和输出
            演示了如何在Python代码中运行命令nslookup www.python.org，这和命令行直接运行的效果是一样的
                import subprocess
                
                print('$ nslookup www.python.org')
                r = subprocess.call(['nslookup', 'www.python.org'])
                print('Exit code:', r)
                
    5.进程间通信
        (1) Python的multiprocessing模块包装了底层的机制，提供了Queue、Pipes等多种方式来交换数据
                from multiprocessing import Process, Queue
                import os, time, random
                
                # 写数据进程执行的代码:
                def write(q):
                    print('Process to write: %s' % os.getpid())
                    for value in ['A', 'B', 'C']:
                        print('Put %s to queue...' % value)
                        q.put(value)
                        time.sleep(random.random())
                
                # 读数据进程执行的代码:
                def read(q):
                    print('Process to read: %s' % os.getpid())
                    while True:
                        value = q.get(True)
                        print('Get %s from queue.' % value)
                
                if __name__=='__main__':
                    # 父进程创建Queue，并传给各个子进程：
                    q = Queue()
                    pw = Process(target=write, args=(q,))
                    pr = Process(target=read, args=(q,))
                    # 启动子进程pw，写入:
                    pw.start()
                    # 启动子进程pr，读取:
                    pr.start()
                    # 等待pw结束:
                    pw.join()
                    # pr进程里是死循环，无法等待其结束，只能强行终止:
                    pr.terminate()
                    
    6.多线程
        (1) Python的标准库提供了两个模块：_thread和threading，_thread是低级模块，threading是高级模块，
            对_thread进行了封装。绝大多数情况下，我们只需要使用threading这个高级模块
            
                import time, threading
                
                # 新线程执行的代码:
                def loop():
                    print('thread %s is running...' % threading.current_thread().name)
                    n = 0
                    while n < 5:
                        n = n + 1
                        print('thread %s >>> %s' % (threading.current_thread().name, n))
                        time.sleep(1)
                    print('thread %s ended.' % threading.current_thread().name)
                
                print('thread %s is running...' % threading.current_thread().name)
                t = threading.Thread(target=loop, name='LoopThread')
                t.start()
                t.join()
                print('thread %s ended.' % threading.current_thread().name)
                
            Python的threading模块有个current_thread()函数，它永远返回当前线程的实例
            
            创建一个锁就是通过threading.Lock()来实现：
            
                balance = 0
                lock = threading.Lock()
                
                def run_thread(n):
                    for i in range(100000):
                        # 先要获取锁:
                        lock.acquire()
                        try:
                            # 放心地改吧:
                            change_it(n)
                        finally:
                            # 改完了一定要释放锁:
                            lock.release()
                            
                            
        (2) 使用:
                A.threading.Thread(target=loop, name='LoopThread')
                B.threading.Thread(target=loop, args=(3,))
                
        (3) 
            Python解释器由于设计时有GIL(Global Interpreter Lock)全局锁，导致了多线程无法利用多核,
            任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行
            
    7.ThreadLocal
    
            import threading
            
            # 创建全局ThreadLocal对象:
            local_school = threading.local()
            
            def process_student():
                # 获取当前线程关联的student:
                std = local_school.student
                print('Hello, %s (in %s)' % (std, threading.current_thread().name))
            
            def process_thread(name):
                # 绑定ThreadLocal的student:
                local_school.student = name
                process_student()
            
            t1 = threading.Thread(target= process_thread, args=('Alice',), name='Thread-A')
            t2 = threading.Thread(target= process_thread, args=('Bob',), name='Thread-B')
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            
    全局变量local_school就是一个ThreadLocal对象,每个Thread对它都可以读写student属性，但互不影响。
    你可以把local_school看成全局变量，但每个属性如local_school.student都是线程的局部变量，可以任意读写而互不干扰，
    也不用管理锁的问题，ThreadLocal内部会处理。
    
    ThreadLocal最常用的地方就是为每个线程绑定一个数据库连接，HTTP请求，用户身份信息等，
    这样一个线程的所有调用到的处理函数都可以非常方便地访问这些资源
    
    一个ThreadLocal变量虽然是全局变量，但每个线程都只能读写自己线程的独立副本，互不干扰。
    ThreadLocal解决了参数在一个线程中各个函数之间互相传递的问题。
    
    8.分布式进程
        通过managers模块把Queue通过网络暴露出去，就可以让其他机器的进程访问Queue
            服务进程
                # task_master.py
                
                import random, time, queue
                from multiprocessing.managers import BaseManager
                
                # 发送任务的队列:
                task_queue = queue.Queue()
                # 接收结果的队列:
                result_queue = queue.Queue()
                
                # 从BaseManager继承的QueueManager:
                class QueueManager(BaseManager):
                    pass
                
                # 把两个Queue都注册到网络上, callable参数关联了Queue对象:
                QueueManager.register('get_task_queue', callable=lambda: task_queue)
                # 其中get_task_queue 是自己命名的 函数名
                QueueManager.register('get_result_queue', callable=lambda: result_queue)
                # 绑定端口5000, 设置验证码'abc':
                # 监听端口 5000
                manager = QueueManager(address=('', 5000), authkey=b'abc')
                # 启动Queue:
                manager.start()
                # 获得通过网络访问的Queue对象:
                task = manager.get_task_queue()
                result = manager.get_result_queue()
                # 放几个任务进去:
                for i in range(10):
                    n = random.randint(0, 10000)
                    print('Put task %d...' % n)
                    task.put(n)
                # 从result队列读取结果:
                print('Try get results...')
                for i in range(10):
                    r = result.get(timeout=10)
                    print('Result: %s' % r)
                # 关闭:
                manager.shutdown()
                print('master exit.')
                
            任务进程:
                # task_worker.py
                
                import time, sys, queue
                from multiprocessing.managers import BaseManager
                
                # 创建类似的QueueManager:
                class QueueManager(BaseManager):
                    pass
                
                # 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
                QueueManager.register('get_task_queue')
                QueueManager.register('get_result_queue')
                
                # 连接到服务器，也就是运行task_master.py的机器:
                server_addr = '127.0.0.1'
                print('Connect to server %s...' % server_addr)
                # 端口和验证码注意保持与task_master.py设置的完全一致:
                m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
                # 从网络连接:
                m.connect()
                # 获取Queue的对象:
                task = m.get_task_queue()
                result = m.get_result_queue()
                # 从task队列取任务,并把结果写入result队列:
                for i in range(10):
                    try:
                        n = task.get(timeout=1)
                        print('run task %d * %d...' % (n, n))
                        r = '%d * %d = %d' % (n, n, n*n)
                        time.sleep(1)
                        result.put(r)
                    except Queue.Empty:
                        print('task queue is empty.')
                # 处理结束:
                print('worker exit.')

```

### virtualenv

```shell
    windows安装使用virtualenv
        1.新建虚拟环境
             在当前目录下右键打开cmd，输入virtualenv 虚拟环境名字
            
        2.激活虚拟环境
            1）在当前目录下进入脚本目录 Scripts，并运行activate.bat(只需要输入 activate.bat)
            结果:
                (虚拟环境名字) 绝对路径名
            
        3.退出虚拟环境
            在Scripts对应的cmd中输入 deactivate.bat
            
    linux安装使用virtualenv
        1.> sudo apt-get install python-virtualenv
        2.创建虚拟环境
            > virtualenv 虚拟环境名(采用默认的python)
        3.进入虚拟环境空间
            在对应目录的bin
            > source activate
        4.需要创建其他python版本的虚拟环境
            virtualenv -p /usr/bin/python3 虚拟环境名(采用默认的python)
            
        5.退出虚拟环境
           (虚拟环境名字)  > deactivate
            
        
            
    B. 安装使用virtualenvwrapper(虚拟环境管理包)
            (1) windows下
                     pip install virtualenvwrapper-win
                    
            (2) 
                    A.加入环境变量中
                        将virtualenvwrapper-win的安装目录加入到系统变量中，这样在cmd中就可以直接输入mkvirtualenv命令，不需要加入
                         绝对路径
                                将其C:\Users\Jame\AppData\Local\Programs\Python\Python35-32\Scripts (安装路径)
                                      加入到 计算机(属性)-> 高级系统设置->环境变量->系统变量(path)编辑
                        
                        
                    (2)设置workon_home环境变量(在进行mkvirtualenv创建虚拟环境后文件夹放在指定目录中)
                            计算机(属性)-> 高级系统设置->环境变量->系统变量进行新建
                            变量名: WORKON_HOME
                            变量值: D:\python_example 
                        
            (3) 新建虚拟环境
                    A.mkvirtualenv env2_test (这种情况下是使用默认路径环境变量的python)
                    B.mkvirtualenv --python=(python3安装路径到可执行文件) (虚拟环境名字)
                      mkvirtualenv -p (python3安装路径到可执行文件) (虚拟环境名字)
                       例如：
                        mkvirtualenv 
                                    --python=C:\Users\Administrator\AppData\Local\Programs\Python\Python35\python.exe 
                                    python35_test
            (4) 查看安装的所有虚拟环境
                    workon
            (5) 进入虚拟环境
                    workon 虚拟环境名
            (6) 退出虚拟环境
                    deactivate
                    
                    
            linux下
                    (1) 安装
                        > pip install virtualenvwrapper
                    (2) 找到virtualenvwrapper的执行脚本
                        > sudo find / -name virtualenvwrapper.sh
                            结果:
                                /usr/local/bin/virtualenvwrapper.sh
                           
                    (3) > vim ~/.bashrc
                             export WORKON_HOME=$HOME/.virtualenvs  
                             source /usr/local/bin/virtualenvwrapper.sh
                             
                    (4) > mkvirtualenv pyscrapy
                            结果:
                                Running virtualenv with interpreter /usr/bin/python2
                                New python executable in /home/jame/.virtualenvs/pyscrapy/bin/python2
                                Also creating executable in /home/jame/.virtualenvs/pyscrapy/bin/python
                                Installing setuptools, pkg_resources, pip, wheel...done.
                                virtualenvwrapper.user_scripts creating /home/jame/.virtualenvs/pyscrapy/bin/predeactivate
                                virtualenvwrapper.user_scripts creating /home/jame/.virtualenvs/pyscrapy/bin/postdeactivate
                                virtualenvwrapper.user_scripts creating /home/jame/.virtualenvs/pyscrapy/bin/preactivate
                                virtualenvwrapper.user_scripts creating /home/jame/.virtualenvs/pyscrapy/bin/postactivate
                                virtualenvwrapper.user_scripts creating /home/jame/.virtualenvs/pyscrapy/bin/get_env_details
                                
                    (5) 
                            
    

```

### 协程

```shell
    1.协程看上去也是子程序,但执行过程中,在子程序内部可中断,然后转而执行别的子程序,在适当的时候再返回来接着执行
    2.优点:
        A.协程极高的执行效率。因为子程序切换不是线程切换，而是由程序自身控制，因此，没有线程切换的开销，
          和多线程比，线程数量越多，协程的性能优势就越明显
        B.不需要多线程的锁机制，因为只有一个线程，也不存在同时写变量冲突，在协程中控制共享资源不加锁，只需要判断状态就好了,
          所以执行效率比多线程高很多.
          
    3.Python的yield不但可以返回一个值，它还可以接收调用者发出的参数
        用协程，生产者生产消息后，直接通过yield跳转到消费者开始执行，待消费者执行完毕后，
        切换回生产者继续生产，效率极高
        
            consumer函数是一个generator
            def consumer():
                r = ''
                while True:
                    n = yield r
                    if not n:
                        return
                    print('[CONSUMER] Consuming %s...' % n)
                    r = '200 OK'
            
            def produce(c):
                c.send(None)   ## 启动生成器
                n = 0
                while n < 5:
                    n = n + 1
                    print('[PRODUCER] Producing %s...' % n)
                    r = c.send(n)
                    print('[PRODUCER] Consumer return: %s' % r)
                c.close()
            
            c = consumer()
            produce(c)
            
    4.yield from用于重构生成器
    
        def copy_fib(n):
        	print('I am copy from fib')
        	yield from fib(n)
        	print('Copy end')
        print('-'*10 + 'test yield from' + '-'*10)
        for fib_res in copy_fib(20):
        	print(fib_res)
        	
       yield from的作用还体现可以像一个管道一样将send信息传递给内层协程，并且处理好了各种异常情况，
       因此，对于stupid_fib也可以这样包装和使用：
       
            def copy_stupid_fib(n):
            	print('I am copy from stupid fib')
            	yield from stupid_fib(n)
            	print('Copy end')
            print('-'*10 + 'test yield from and send' + '-'*10)
            N = 20
            csfib = copy_stupid_fib(N)
            fib_res = next(csfib)
            while True:
            	print(fib_res)
            	try:
            		fib_res = csfib.send(random.uniform(0, 0.5))
            	except StopIteration:
            		break
            
    5.asyncio是Python 3.4版本引入的标准库，直接内置了对异步IO的支持。
        asyncio的编程模型就是一个消息循环。我们从asyncio模块中直接获取一个EventLoop的引用，
        然后把需要执行的协程扔到EventLoop中执行，就实现了异步IO
        
        import asyncio
        
        @asyncio.coroutine
        def hello():
            print("Hello world!")
            # 异步调用asyncio.sleep(1):
            r = yield from asyncio.sleep(1)
            print("Hello again!")
        
        # 获取EventLoop:
        loop = asyncio.get_event_loop()
        # 执行coroutine
        loop.run_until_complete(hello())
        loop.close()
        
    6. asyncio是一个基于事件循环的实现异步I/O的模块。通过yield from，我们可以将协程asyncio.sleep的控制权交给事件循环，
       然后挂起当前协程；之后，由事件循环决定何时唤醒asyncio.sleep,接着向后执行代码。
    
        @asyncio.coroutine
          def smart_fib(n):
            index = 0
            a = 0
            b = 1
            while index < n:
                sleep_secs = random.uniform(0, 0.2)
                yield from asyncio.sleep(sleep_secs)
                print('Smart one think {} secs to get {}'.format(sleep_secs, b))
                a, b = b, a + b
                index += 1
          
          @asyncio.coroutine
          def stupid_fib(n):
            index = 0
            a = 0
            b = 1
            while index < n:
                sleep_secs = random.uniform(0, 0.4)
                yield from asyncio.sleep(sleep_secs)
                print('Stupid one think {} secs to get {}'.format(sleep_secs, b))
                a, b = b, a + b
                index += 1
          
          if __name__ == '__main__':
            loop = asyncio.get_event_loop()
            tasks = [
                asyncio.async(smart_fib(10)),
                asyncio.async(stupid_fib(10)),
            ]
            loop.run_until_complete(asyncio.wait(tasks))
            print('All fib finished.')
            loop.close()
            
        (1) asyncio是一个由python实现的模块，那么我们来看看asyncio.sleep中都做了些什么：
            sleep创建了一个Future对象，作为更内层的协程对象，通过yield from交给了事件循环；
            其次，它通过调用事件循环的call_later函数，注册了一个回调函数
                @coroutine
                def sleep(delay, result=None, *, loop=None):
                    """Coroutine that completes after a given time (in seconds)."""
                    future = futures.Future(loop=loop)
                    h = future._loop.call_later(delay,
                                                future._set_result_unless_cancelled, result)
                    try:
                        return (yield from future)
                    finally:
                        h.cancel()
                        
        (2) 通过查看Future类的源码，可以看到，Future是一个实现了__iter__对象的生成器：
            当我们的协程yield from asyncio.sleep时，事件循环其实是与Future对象建立了练习。
            每次事件循环调用send(None)时，其实都会传递到Future对象的__iter__函数调用；
            而当Future尚未执行完毕的时候，就会yield self，也就意味着暂时挂起，等待下一次send(None)的唤醒。
                class Future:
                	#blabla...
                    def __iter__(self):
                        if not self.done():
                            self._blocking = True
                            yield self  # This tells Task to wait for completion.
                        assert self.done(), "yield from wasn't used with future"
                        return self.result()  # May raise too.
                        
        (3) 当我们包装一个Future对象产生一个Task对象时，在Task对象初始化中，就会调用Future的send(None),
            并且为Future设置好回调函数
                class Task(futures.Future):
                	#blabla...
                    def _step(self, value=None, exc=None):
                		#blabla...
                        try:
                            if exc is not None:
                                result = coro.throw(exc)
                            elif value is not None:
                                result = coro.send(value)
                            else:
                                result = next(coro)
                		#exception handle
                        else:
                            if isinstance(result, futures.Future):
                                # Yielded Future must come from Future.__iter__().
                                if result._blocking:
                                    result._blocking = False
                                    result.add_done_callback(self._wakeup)
                		#blabla...
                 
                    def _wakeup(self, future):
                        try:
                            value = future.result()
                        except Exception as exc:
                            # This may also be a cancellation.
                            self._step(None, exc)
                        else:
                            self._step(value, None)
                        self = None  # Needed to break cycles when an exception occurs.
                        
       (4) 预设的时间过后，事件循环将调用Future._set_result_unless_cancelled:
           这将改变Future的状态，同时回调之前设定好的Tasks._wakeup；在_wakeup中，将会再次调用Tasks._step，这时，
           Future的状态已经标记为完成，因此，将不再yield self，而return语句将会触发一个StopIteration异常，
           此异常将会被Task._step捕获用于设置Task的结果。同时，整个yield from链条也将被唤醒，协程将继续往下执行。
                class Future:
                	#blabla...
                    def _set_result_unless_cancelled(self, result):
                        """Helper setting the result only if the future was not cancelled."""
                        if self.cancelled():
                            return
                        self.set_result(result)
                
                    def set_result(self, result):
                        """Mark the future done and set its result.
                
                        If the future is already done when this method is called, raises
                        InvalidStateError.
                        """
                        if self._state != _PENDING:
                            raise InvalidStateError('{}: {!r}'.format(self._state, self))
                        self._result = result
                        self._state = _FINISHED
                        self._schedule_callbacks()
                        
       (5) async和await
                async def smart_fib(n):
                	index = 0
                	a = 0
                	b = 1
                	while index < n:
                		sleep_secs = random.uniform(0, 0.2)
                		await asyncio.sleep(sleep_secs)
                		print('Smart one think {} secs to get {}'.format(sleep_secs, b))
                		a, b = b, a + b
                		index += 1
                 
                async def stupid_fib(n):
                	index = 0
                	a = 0
                	b = 1
                	while index < n:
                		sleep_secs = random.uniform(0, 0.4)
                		await asyncio.sleep(sleep_secs)
                		print('Stupid one think {} secs to get {}'.format(sleep_secs, b))
                		a, b = b, a + b
                		index += 1
                 
                if __name__ == '__main__':
                	loop = asyncio.get_event_loop()
                	tasks = [
                		asyncio.ensure_future(smart_fib(10)),
                		asyncio.ensure_future(stupid_fib(10)),
                	]
                	loop.run_until_complete(asyncio.wait(tasks))
                	print('All fib finished.')
                	loop.close()

```