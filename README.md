# python
 
## pyhton 简介

```shell

    Python为我们提供了非常完善的基础代码库,覆盖了网络、文件、GUI、数据库、文本等大量内容,
    被形象地称作“内置电池（batteries included）
    
    那Python适合开发哪些类型的应用呢？
        首选是网络应用，包括网站、后台服务等等；
        其次是许多日常需要的小工具，包括系统管理员需要的脚本任务等等；
        另外就是把其他语言开发的程序再包装起来,方便使用.
        
    Python的缺点
        1.运行速度慢,和C程序相比非常慢,因为Python是解释型语言,你的代码在执行时会一行一行地翻译成CPU能理解的机器码,
          这个翻译过程非常耗时,所以很慢.而C程序是运行前直接编译成CPU能执行的机器码,所以非常快
        2.代码不能加密,如果要发布你的Python程序,实际上就是发布源代码(跟shell脚本一样),这一点跟C语言不同,C语言不用发布源代码,
          只需要把编译后的机器码（可执行的二进制文件）发布出去
          
    Python交互模式
        在命令行模式(终端)输入 python, 则 进入到Python交互模式,它的提示符是>>>

```

## python 安装

```shell

    1. 配置软件仓库，因为python 3.6 新版没有发布到ubuntu的正式仓库中，咱们通过第3方仓库来做
       > sudo add-apt-repository ppa:jonathonf/python-3.6
    2. > sudo apt-get update
    3. > sudo apt-get install python3.6
    4. 查看python版本信息
        >  python3 -V
        结果:
            Python 3.5.2
            
        > python3.6 -V
        结果:
            Python 3.6.3
            
    5.配置输入python3时就默认使用3.6版本
        > sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
        > sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
        > sudo update-alternatives --config python3
        > python3 -V
        结果:
            Python 3.6.3
            
            
    如果想直接输入 python 就直接对应到 python3.6
        > sudo rm /usr/bin/python 
        > cd /usr/bin
        > ln -s python3.2 python  # Choose the Python 3.x binary here

```

## python 运行

```shell

    1.显示调用 python3 命令 
        > python3 calc.py
    
    2.直接运行 calc.py 文件
        (1) 在calc.py 文件内容中第一行加上一个特殊的注释 
                #!/usr/bin/env python3
        (2) 赋值可执行权限
                > chmod +x calc.py
        (3) 运行
                > ./calc.py

```