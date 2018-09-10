# Django
 
## Django 搭建开发环境

```shell

    1. 创建虚拟环境(以 python2.7 )
         > mkvirtualenv --python=C:\Python27\python.exe django_test_27
         
    2. 进入虚拟环境
        > workon django_test_27
        
    3. 在虚拟环境中安装 django
        (django_test_27) λ pip install django==1.9.8
        
    4.在 PyCharm 中新建 Django
       A. File -> New Project  
       B. Existing interpreter  再选中创建的虚拟环境
       
    注意:
        1.在 Django 服务启动时，默认访问IP只能是127.0.0.1:8000,如果需要用外网ip进行访问则，
          则在 Run-> Edit Configuration 中的 Host 写为 0.0.0.0:8000， 则该 Django是部署在
          192.168.0.2 中，则可以通过 http://192.168.0.2:8000 进行访问

```

## 结构层次

```shell
    1.templates 存放 html 文件
    2.project_dir/settings.py : 放置了 Django 的全局配置信息
      project_dir/urls.py : 放置了 Django 的主要的 url 入口
      project_dir/wsgi.py : 放置了 Django 启动的 wsgi 文件
    3. manager.py : 启动 Django 的主要文件，主要的命令都是通过 manager.py 来运行的
    4.
        (1) 创建 App 目录，在 PyCharm 中 Tools-> Run manager Task 来运行 Django 命令
            (1) 新建app
                    > startapp message
                    
        (2) 新建 apps 目录存放 message 目录，在 PyCharm 中 该项目右键新建目录 message 
            其中在 apps 目录下自动生成 __init.py 文件，说明将 apps 作为可导入的包
            
            方便编码：
                在其他文件中要引入 message 文件 ---> from apps.message import views
                
                如果想在在其他文件中要引入 message 文件---> from message import views
                在 apps 文件夹下右键 Mark Directory As -> Sources Root, 这样是 PyCharm 
                IDE 中是不会报错，
                但是在命令行会报错。
                    (1) > workon django_test_27
                    (2) >  cd D:\python_example\untitled1(具体项目位置)
                    (3) > (django_test_27) λ python manage.py runserver
                                Traceback (most recent call last):
                                  File "manage.py", line 5, in <module>
                                    from message import views
                                ImportError: No module named message
                                原因： 因为在 PyCharm 中已经将 apps 设置为 Source Root，所以 IDE 不会报错，
                                      但是在命令行中是使用 settings.py 中的参数，在 settings.py 中我们没有
                                      将 apps 当作 Source Root 的搜索路径，
            
                    
    5.新建 static 目录来存放 css 文件， js 文件，图片文件， 在 PyCharm 中 该项目右键新建目录 static 
    6.新建 log 目录存放日志， 在 PyCharm 中 该项目右键新建目录 log 
    7. 新建 media 用于存放用户上传文件, 在 PyCharm 中 该项目右键新建目录 meida 
```
