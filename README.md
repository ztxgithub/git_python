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
                # -*- coding: utf-8 -*-
        (2) 赋值可执行权限
                > chmod +x calc.py
        (3) 运行
                > ./calc.py

```

[参考资料](https://www.jianshu.com/p/ae46c479252d)

## 集成IDE(PyCharm)安装

```shell
    1.下载地址
        https://www.jetbrains.com/pycharm/download/#section=windows
        
    2.
        (1)启动PyCharm
            > ./bin/pycharm.sh
        (2) 创建快捷键
            > vim ~/.bashrc
                alias pycharm="bash /home/jame/soft/pycharm-2018.1.2/bin/pycharm.sh"
                
            > source ~/.bashrc

        (3) 激活
                Help->Register

                Activation code
                K71U8DBPNE-eyJsaWNlbnNlSWQiOiJLNzFVOERCUE5FIiwibGljZW5zZWVOYW1lIjoibGFuIHl1IiwiYXNzaWduZWVOYW1lIjoiIiwiYXNzaWduZWVFbWFpbCI6IiIsImxpY2Vuc2VSZXN0cmljdGlvbiI6IkZvciBlZHVjYXRpb25hbCB1c2Ugb25seSIsImNoZWNrQ29uY3VycmVudFVzZSI6ZmFsc2UsInByb2R1Y3RzIjpbeyJjb2RlIjoiSUkiLCJwYWlkVXBUbyI6IjIwMTktMDUtMDQifSx7ImNvZGUiOiJSUzAiLCJwYWlkVXBUbyI6IjIwMTktMDUtMDQifSx7ImNvZGUiOiJXUyIsInBhaWRVcFRvIjoiMjAxOS0wNS0wNCJ9LHsiY29kZSI6IlJEIiwicGFpZFVwVG8iOiIyMDE5LTA1LTA0In0seyJjb2RlIjoiUkMiLCJwYWlkVXBUbyI6IjIwMTktMDUtMDQifSx7ImNvZGUiOiJEQyIsInBhaWRVcFRvIjoiMjAxOS0wNS0wNCJ9LHsiY29kZSI6IkRCIiwicGFpZFVwVG8iOiIyMDE5LTA1LTA0In0seyJjb2RlIjoiUk0iLCJwYWlkVXBUbyI6IjIwMTktMDUtMDQifSx7ImNvZGUiOiJETSIsInBhaWRVcFRvIjoiMjAxOS0wNS0wNCJ9LHsiY29kZSI6IkFDIiwicGFpZFVwVG8iOiIyMDE5LTA1LTA0In0seyJjb2RlIjoiRFBOIiwicGFpZFVwVG8iOiIyMDE5LTA1LTA0In0seyJjb2RlIjoiR08iLCJwYWlkVXBUbyI6IjIwMTktMDUtMDQifSx7ImNvZGUiOiJQUyIsInBhaWRVcFRvIjoiMjAxOS0wNS0wNCJ9LHsiY29kZSI6IkNMIiwicGFpZFVwVG8iOiIyMDE5LTA1LTA0In0seyJjb2RlIjoiUEMiLCJwYWlkVXBUbyI6IjIwMTktMDUtMDQifSx7ImNvZGUiOiJSU1UiLCJwYWlkVXBUbyI6IjIwMTktMDUtMDQifV0sImhhc2giOiI4OTA4Mjg5LzAiLCJncmFjZVBlcmlvZERheXMiOjAsImF1dG9Qcm9sb25nYXRlZCI6ZmFsc2UsImlzQXV0b1Byb2xvbmdhdGVkIjpmYWxzZX0=-Owt3/+LdCpedvF0eQ8635yYt0+ZLtCfIHOKzSrx5hBtbKGYRPFDrdgQAK6lJjexl2emLBcUq729K1+ukY9Js0nx1NH09l9Rw4c7k9wUksLl6RWx7Hcdcma1AHolfSp79NynSMZzQQLFohNyjD+dXfXM5GYd2OTHya0zYjTNMmAJuuRsapJMP9F1z7UTpMpLMxS/JaCWdyX6qIs+funJdPF7bjzYAQBvtbz+6SANBgN36gG1B2xHhccTn6WE8vagwwSNuM70egpahcTktoHxI7uS1JGN9gKAr6nbp+8DbFz3a2wd+XoF3nSJb/d2f/6zJR8yJF8AOyb30kwg3zf5cWw==-MIIEPjCCAiagAwIBAgIBBTANBgkqhkiG9w0BAQsFADAYMRYwFAYDVQQDDA1KZXRQcm9maWxlIENBMB4XDTE1MTEwMjA4MjE0OFoXDTE4MTEwMTA4MjE0OFowETEPMA0GA1UEAwwGcHJvZDN5MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxcQkq+zdxlR2mmRYBPzGbUNdMN6OaXiXzxIWtMEkrJMO/5oUfQJbLLuMSMK0QHFmaI37WShyxZcfRCidwXjot4zmNBKnlyHodDij/78TmVqFl8nOeD5+07B8VEaIu7c3E1N+e1doC6wht4I4+IEmtsPAdoaj5WCQVQbrI8KeT8M9VcBIWX7fD0fhexfg3ZRt0xqwMcXGNp3DdJHiO0rCdU+Itv7EmtnSVq9jBG1usMSFvMowR25mju2JcPFp1+I4ZI+FqgR8gyG8oiNDyNEoAbsR3lOpI7grUYSvkB/xVy/VoklPCK2h0f0GJxFjnye8NT1PAywoyl7RmiAVRE/EKwIDAQABo4GZMIGWMAkGA1UdEwQCMAAwHQYDVR0OBBYEFGEpG9oZGcfLMGNBkY7SgHiMGgTcMEgGA1UdIwRBMD+AFKOetkhnQhI2Qb1t4Lm0oFKLl/GzoRykGjAYMRYwFAYDVQQDDA1KZXRQcm9maWxlIENBggkA0myxg7KDeeEwEwYDVR0lBAwwCgYIKwYBBQUHAwEwCwYDVR0PBAQDAgWgMA0GCSqGSIb3DQEBCwUAA4ICAQC9WZuYgQedSuOc5TOUSrRigMw4/+wuC5EtZBfvdl4HT/8vzMW/oUlIP4YCvA0XKyBaCJ2iX+ZCDKoPfiYXiaSiH+HxAPV6J79vvouxKrWg2XV6ShFtPLP+0gPdGq3x9R3+kJbmAm8w+FOdlWqAfJrLvpzMGNeDU14YGXiZ9bVzmIQbwrBA+c/F4tlK/DV07dsNExihqFoibnqDiVNTGombaU2dDup2gwKdL81ua8EIcGNExHe82kjF4zwfadHk3bQVvbfdAwxcDy4xBjs3L4raPLU3yenSzr/OEur1+jfOxnQSmEcMXKXgrAQ9U55gwjcOFKrgOxEdek/Sk1VfOjvS+nuM4eyEruFMfaZHzoQiuw4IqgGc45ohFH0UUyjYcuFxxDSU9lMCv8qdHKm+wnPRb0l9l5vXsCBDuhAGYD6ss+Ga+aDY6f/qXZuUCEUOH3QUNbbCUlviSz6+GiRnt1kA9N2Qachl+2yBfaqUqr8h7Z2gsx5LcIf5kYNsqJ0GavXTVyWh7PYiKX4bs354ZQLUwwa/cG++2+wNWP+HtBhVxMRNTdVhSm38AknZlD+PTAsWGu9GyLmhti2EnVwGybSD2Dxmhxk3IPCkhKAK+pl0eWYGZWG3tJ9mZ7SowcXLWDFAk0lRJnKGFMTggrWjV8GYpw5bq23VmIqqDLgkNzuoog==
        (4) 通过 Settings->interpreter 加载python解释器
```

## 安装mysql for windows

```shell
    1.下载地址
        https://dev.mysql.com/downloads/windows/
        点击 MySQL Installer

        https://dev.mysql.com/downloads/installer/

```

## 安装 navicat for mysql