# python 模块
 
## pyhton 模块概念

```shell

    1.一个.py文件就称之为一个模块（Module）
    2.使用模块还可以避免函数名和变量名冲突。相同名字的函数和变量完全可以分别存在不同的模块中，
      因此，我们自己在编写模块时，不必考虑名字会与其他模块冲突。但是也要注意，尽量不要与内置函数名字冲突
      
    3.避免模块名冲突，Python又引入了按目录来组织模块的方法，称为包（Package）
      假设我们的abc和xyz这两个模块名字与其他模块冲突了,于是我们可以通过包来组织模块，避免冲突.
      方法是选择一个顶层包名，比如mycompany
      引入了包以后，只要顶层的包名不与别人冲突,那所有模块都不会与别人冲突。现在，
      abc.py模块的名字就变成了mycompany.abc，类似的，xyz.py的模块名变成了mycompany.xyz
      每一个包目录下面都会有一个__init__.py的文件，这个文件是必须存在的，否则，Python就把这个目录当成普通目录，
      而不是一个包。__init__.py可以是空文件，也可以有Python代码，因为__init__.py本身就是一个模块，
      而它的模块名就是mycompany.
      
    4. 自己创建模块时要注意命名,不能和Python自带的模块名称冲突。例如，系统自带了sys模块，自己的模块就不可命名为sys.py,
       否则将无法导入系统自带的sys模块。

```

## 使用模块

```shell

    1.
        #!/usr/bin/env python3
        # -*- coding: utf-8 -*-
        
        ' a test module '            (一个字符串，表示模块的文档注释，任何模块代码的第一个字符串都被视为模块的文档注释；)
        
        __author__ = 'Michael Liao'
        
        import sys    (我们就有了变量sys指向该模块，利用sys这个变量，就可以访问sys模块的所有功能)
        
        def test():
            args = sys.argv
            if len(args)==1:
                print('Hello, world!')
            elif len(args)==2:
                print('Hello, %s!' % args[1])
            else:
                print('Too many arguments!')
        
        if __name__=='__main__':
            test()
            
            
        当我们在命令行运行hello模块文件时，Python解释器把一个特殊变量__name__置为__main__，
        而如果在其他地方导入该hello模块时，if判断将失败，因此，这种if测试可以让一个模块通过命令行运行时执行一些额外的代码，
        最常见的就是运行测试。
        
        A.启动Python交互环境，再导入hello模块
                $ python3
                Python 3.4.3 (v3.4.3:9b73f1c3e601, Feb 23 2015, 02:52:03) 
                [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
                Type "help", "copyright", "credits" or "license" for more information.
                >>> import hello   (导入时，没有打印Hello, word!，因为没有执行test()函数)
                >>> hello.test()    (调用hello.test()时，才能打印出Hello, word!)
                结果
                Hello, world!
                
    2.作用域
        在一个模块中,我们可能会定义很多函数和变量,但有的函数和变量我们希望给别人使用，
        有的函数和变量我们希望仅仅在模块内部使用。在Python中，是通过_前缀来实现的
        类似_xxx和__xxx这样的函数或变量就是非公开的（private），不应该被直接引用，比如_abc，__abc等

```

## 安装第三方模块

```shell

    1.在Python中，安装第三方模块，是通过包管理工具pip完成的
    2.Linux上有可能并存Python 3.x和Python 2.x，因此对应的pip命令是pip3
    3.要安装一个第三方库，必须先知道该库的名称，可以在官网或者pypi上搜索，比如Pillow的名称叫Pillow，
      因此，安装Pillow的命令就是：
        > pip install Pillow
        
    4.安装常用模块,推荐直接使用Anaconda，这是一个基于Python的数据处理和科学计算平台，它已经内置了许多非常有用的第三方库，
      我们装上Anaconda，就相当于把数十个第三方模块自动安装好了，非常简单易用。
      
    5.模块搜索路径
       A.Python解释器会搜索当前目录、所有已安装的内置模块和第三方模块，搜索路径存放在sys模块的path变量中
            >>> import sys
            >>> sys.path
            
       B.如果我们要添加自己的搜索目录
            (1) 直接修改sys.path，添加要搜索的目录 这种方法是在运行时修改，运行结束后失效:
                    >>> import sys
                    >>> sys.path.append('/Users/michael/my_py_scripts')
            (2) windows设置环境变量PYTHONPATH，该环境变量的内容会被自动添加到模块搜索路径中。
                设置方式与设置Path环境变量类似。注意只需要添加你自己的搜索路径，Python自己本身的搜索路径不受影响

```