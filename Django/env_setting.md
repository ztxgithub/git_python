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

## Django 项目的运行

```shell
    1. workon 虚拟环境
    2. 在虚拟环境中安装好对应的软件包
        > pip install -r  requirements.txt
            
        requirements.txt 的内容
            Django==1.9.8
            
    3.(django_start) λ python manage.py runserver
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

## Django 配置数据库（为 model 对象做准备）

```shell
    1. 在 project_dir/settings.py 中修改 DATABASES 为
            DATABASES = {
                            'default': {
                                'ENGINE': 'django.db.backends.mysql',
                                'NAME': "testdjango",    # 数据库名
                                'USER':"root",           # 用户名
                                'PASSWORD':"123456",     # 密码
                                'HOST':"127.0.0.1"       # 连接主机 ip
                            }
                        }
            
    2. 根据数据库来直接生成好 django 默认的数据表，在 PyCharm Tools->Run manager.py Task
            (1) 问题一:
                    django.core.exceptions.ImproperlyConfigured: 
                    Error loading MySQLdb module: No module named MySQLdb
                原因:
                    没有安装 MySQLdb 的驱动
                    
                解决方案:
                    在虚拟环境中安装驱动
                    (django_test_27) λ pip install mysql-python
                        1.安装 mysql-python (pip install mysql-python) 时报错
                         error: Microsoft Visual C++ 9.0 is required. Get it from http://aka.ms/vcpython27
                         
                         解决方案:下载安装包进行本地安装
                            第一步: 在 http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python下载对应的包版本，
                                    如果是win7 64位2.7版本的python，就下载
                                            MySQL_python-1.2.5-cp27-none-win_amd64.whl
                
                            第二步: 在命令行执行pip install MySQL_python-1.2.5-cp27-none-win_amd64.whl
                                   当然需要在cmd下跳转到下载MySQL_python-1.2.5-cp27-none-win_amd64.whl的目录下
                                   
            (2) 问题二：
                    Error fetching command 'collectstatic': You're using the staticfiles app 
                    without having set the STATIC_ROOT setting to a filesystem path.
                    Command 'collectstatic' skipped
                    
                解决方案:
                    在settings.py中增加
                          STATIC_ROOT = os.path.join(BASE_DIR, 'static')
                          
    3. 在 PyCharm 底部的运行框中输入 
            manage.py@untitled1 > migrate
            
       则在对应的数据库中生成了 Django 所需要的表
            
```

## 为 html 创建 url 的映射

```shell
    1.有一个 form.html 页面，要为 form.html 创建一个 url 的映射
    
            (1) 在 apps/message/views.py
                    """
                        这里 request 是 Django 的 http request 对象
                    """
                    def getform(request):
                        """
                        直接方法 页面
                            参数：
                                request： http request 对象
                                template_name：html 页面名称
                        """
                        return render(request, 'message_form.html')
                        
            (2) 在 urls.py 中 新增
                    urlpatterns = [
                            url(r'^form/$', getform)
                        ]
                        
            (3) 在 settings.py 中修改 'DIRS' 的内容(为了找到对应的 message_form.html 文件)
                    TEMPLATES = [
                        {
                            'BACKEND': 'django.template.backends.django.DjangoTemplates',
                            'DIRS': [os.path.join(BASE_DIR, 'templates')]
                            ,
                            'APP_DIRS': True,
                            'OPTIONS': {
                                'context_processors': [
                                    'django.template.context_processors.debug',
                                    'django.template.context_processors.request',
                                    'django.contrib.auth.context_processors.auth',
                                    'django.contrib.messages.context_processors.messages',
                                ],
                            },
                        },
                    ]
                    
            (4)  在 settings.py 中修改中新增 STATICFILES_DIRS
                        STATICFILES_DIRS = [
                            os.path.join(BASE_DIR, 'static')
                            ]
                    
```
