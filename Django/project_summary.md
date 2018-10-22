# Django 教育平台实战
 
## 基础知识

```shell
    1.循环引用: 在 Django app 中，每一个 app 中都会由 models.py ,在 models.py 文件中有可能遇到其他
               app 中的 models.py. 例如在 User app 中的 models.py 定义了 UserCourse ,这个时候
               UserCourse 会用到一个外键(course), 而 course 是定义在 Courses app 中的 models.py 
               CourseComment. 同样 CourseComment 会用到 User app 中的 models.py 定义了 UserCourse
               
      在设计 app 时，避免进行循环引用，采用的方法时分层设计，设计更高层的 app, 同时包含它们
```
 
## Django app

```shell

    1. users-用户管理
         比如 用户的收藏，用户的基本信息
         
    2. course-课程管理
         包括课程的基本信息
         
         courses models.py
            (1) Course :课程基本信息
            (2) Lesson :章节信息
            (3) Video :视频， 用于存放视频的基本信息(视频的链接和访问地址)
            (4) CourseResource : 课程资源
         
    3. organization-机构和教师管理
    
            organization models.py
                (1) CourseOrg: 课程机构基本信息
                (2) Teacher: 教师基本信息
                (3) CityDict: 城市信息
    
    4. operation-用户操作管理（避免循环引用而采取的分层）
           主要用于记录用户的操作信息，比如 users 和 courses 之间的联系， users 和 organization 之间的联系
           
           operation models.py
                (1) UserAsk: 用户咨询 
                (2) CourseComments: 用户评论(用户对课程的评论)
                (3) UseFavorite: 用户收藏
                (4) UserMessage: 用户消息
                (5) UserCourse: 用户学习的课程，用户在点击了我要学习之后记录了用户和课程之间的关系
           
           
    5. app model 分层
            
                operation
                
       courses   organization  users
           

```

### users app

```shell
    1. 在 PyCharm 中 Tools-> Run manager Task 来运行 Django 命令
            manage.py@custom_mxonline > startapp users
            
    2. 编写 users/models.py
            其中 Django 默认生成了 auth_users 表，其中 is_superuser 字段代表是否为超级用户
            is_staff 字段表示是否为员工， is_active 字段表示该用户是否为激活状态
            date_joined 字段表示用户注册的时间
            
            from django.contrib.auth.models import AbstractUser : 通过继承AbstractUser类
            可以拥有 Django 默认生成了 auth_users 表字段名
            
            class UserProfile(AbstractUser):
                # 昵称
                nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
                # 生日
                birday = models.DateField(verbose_name=u"生日", null=True, blank=True)
                
    3. 在 settings.py 进行注册新建的 app
             INSTALLED_APPS = [
                'users'
            ]
            
    4. 在 settings.py 中重载 settings 方法
            # 此处重载是为了使我们的UserProfile生效
            AUTH_USER_MODEL = "users.UserProfile"
            
    5. 
        (1)
            在运行时报错： 
            ERRORS:
                    users.UserProfile.image: (fields.E210) Cannot use ImageField
                     because Pillow is not installed.
                     
            解决方法：
                在虚拟环境中安装 Pillow 
                (django_start) λ pip install Pillow
                
        (2) 在运行时报错：
                ValueError: Dependency on app with no migrations: users
                
            解决方法：
                在 PyCharm 中 Tools->Run manager.py Task,主要是通过以下的命令对
                 数据库表进行变更
            manage.py@untitled1 > makemigrations users(这个是 apps 名字)
            manage.py@DjangoGetStarted > migrate users
            
            manage.py@untitled1 > makemigrations    # 如果不写 app 的名称将生成所有 apps 的 migrations
            
```

## 将 apps 归类

```shell
    1. 右键点击项目 New -> Python Package 
    2. 将 courses 目录，operation 目录，organization 目录，users 目录拖到 apps 中
       在弹出对话框 Search for references, Open moved files in editor 的勾选去掉
       
    3. 问题一：courses 目录下 models.py 中的 "from organization.models import Teacher" 出现
              Unresolved reference 'organization' 的错误
       解决方案：
            在 apps 目录右键  Mark Directory As -> Sources Root
            
       问题二: 即使在 PyCharm IDE 中设置了但在 cmd 中运行 "python manage.py runserver 0.0.0.0:8000" 会报错
       解决方案:
            在 settings.py 中设置将apps路径加入到 python 搜索目录之下
                import sys
                sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
                
            (django_start) λ python manage.py runserver 0.0.0.0:8000
                        
```

## 后台管理系统

```shell
    1.特点
        (1) 权限管理
        (2) 少前端样式
                后台管理首要解决问题是快速搭建
        (3) 快速开发
        
    2. Django admin 
          Django admin 在我们项目建立好就自动生成好了，在 settings.py 中 INSTALLED_APPS 第一个就是 django.contrib.admin
          Django admin 其实就是 app, 在新建项目之后自动在 urls.py 中 添加 admin 的链接( url(r'^admin/', admin.site.urls))
          会指向 admin.site.urls 的配置中，在我们新建好项目后，我们可以直接访问 admin 系统的
          
          A. 访问 admin 系统的操作流程
                (1) 运行服务 Run
                (2) 在浏览器访问 http://127.0.0.1:8000/admin
                (3) 自动创建超级用户
                        在 PyCharm 中 Tools->Run manager.py Task
                                manage.py@custom_mxonline> createsuperuser
                                用户名: root
                                密码: rootadmin
                                
          B. 将网页修改为中文
                (1) 在 settings.py 中
                    将语言有英文改为中文
                    将 LANGUAGE_CODE = 'en-us' 修改为 LANGUAGE_CODE = 'zh-hans'
                    
                    将时区改为上海
                    TIME_ZONE = 'UTC'  修改为 TIME_ZONE = 'Asia/Shanghai'
                    
                    USE_TZ = True  修改为 USE_TZ = False
                    USE_TZ 代表数据库存储使用时间，True 时间会被存为 UTC 的时间，而我们需要采用本地时间保存到数据库
                    
          C. 
            在 Django 管理页面中 组 对应于数据库的 auth_group, 在 Django 的管理系统中可以将 model 的数据表都注册
            Django 管理页面，这样我们就可以对这张表进行增删改查。
            
            将 UserProfile 重新注册进来
                (1) apps/users/admin.py 用于注册后台管理系统
                        # # 因为同一个目录，所以可以直接.models
                             from .models import UserProfile
                            # # 写一个管理器:命名, model+Admin
                             class UserProfileAdmin(admin.ModelAdmin):
                                 pass
                             # 将UserProfile注册进我们的admin中, 并为它选择管理器
                             admin.site.register(UserProfile,UserProfileAdmin)
    
    3.Django Xadmin
        (1) xadmin 是 Django 更强大的后台管理系统
        (2) 安装 xadmin
                I. 方法一
                        A.在虚拟环境中按 xadmin      
                            (django_start) λ pip install xadmin      
                            
                        B. 在 settings.py 配置 app (Django 的一切开发是基于 app)
                                INSTALLED_APPS = [
                                                    'xadmin',
                                                    'crispy_forms'
                                                 ]
                                                 
                        C. 修改 urls.py 改为 xadmin
                                import xadmin
                                urlpatterns = [
                                                url(r'^xadmin/', xadmin.site.urls),
                                              ]
                                              
                        D. 原先 users/admin.py 的注册方式注释掉
                        E. 需要将 xadmin 表进行同步(不然会出现 ProgrammingError: 
                           (1146, "Table 'mxonline_test.xadmin_usersettings' doesn't exist"))
                                 在 PyCharm 中 Tools->Run manager.py Task
                                        manage.py@custom_mxonline> makemigrations
                                        manage.py@custom_mxonline> migrate
                                        
                II. 方法二
                        
                        A. 通过下载 github xadmin 的源码，解压，将 xadmin 目录添加到项目中
                        
        (3) xadmin 使用
                A. 如何注册 model
                       (I). 在 apps/users/ 目录下新建 adminx.py (xadmin 会自动查找 apps 下 adminx.py,
                                                               根据文件的内容来注册我们的 model)
                                                               
                       (2) 创建admin的管理类(简单版)
                                import xadmin
                                from .models import EmailVerifyRecord
                                # 创建admin的管理类,这里不再是继承admin，而是继承object
                                class EmailVerifyRecordAdmin(object):
                                    pass
                                
                                # 将头部与脚部信息进行注册:
                                xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
                                
                       (3) 在浏览器 http://127.0.0.1:8000/xadmin/ 中 model 注册的名字(邮箱验证码)，
                            其实就是对应于 class EmailVerifyRecord 中的 class Meta 的 verbose_name 的值。
                            其中 class Meta 的 verbose_name_plural 其实是 model 的复数形式，如果不对
                            verbose_name_plural 进行赋值的，后台管理程序会将 verbose_name_plural 的值自动设置为
                            在 verbose_name 后面加上 "s" , 例如 "邮箱验证码s", 所以在  
                            http://127.0.0.1:8000/xadmin/ 中 model 注册的名字为"邮箱验证码s"
                            
                            在浏览器邮箱验证码页面中， 邮箱验证码为 " admin(xx@163.com) " 是因为 
                            class EmailVerifyRecord 中  def __unicode__(self) 
                            
                            Django 的 xadmin 后台管理系统实际上就是对每一个表做的一个增删改查的管理器，它不像有的智能
                            管理系统(是以一个功能一个功能来设计的，比如说 php 后台管理系统可以在我们的页面中设置首页
                            每个块的显示应该是什么)， 而 Django 则不同，它只是对表进行增删改查，同时也可以在增删改查
                            增加后台逻辑，这样从某种程度来讲是不依赖于具体业务的
                            
                       (4) 问题一： "Table mxonline.xadmin_log doesn't exist"
                           原因是： 之前使用 pip install xadmin 进行安装，现在改用源码 xadmin, 其数据库表不一致
                           解决方案:
                                A. manage.py@custom_mxonline > makemigrations
                                B. manage.py@untitled1 > migrate
                                
                           问题二:在 Run Manage.py Task 中 "ImportError: No module named xadmin"
                           原因是： 在 settings.py 中没有将 extra_apps 目录加入到系统搜索路径中
                           解决方案:
                                  在 settings.py 中 
                                        sys.path.insert(0,os.path.join(BASE_DIR, 'extra_apps'))
                                        
                       (5) 需要在 users/adminx.py class EmailVerifyRecordAdmin
                           中进行改写
                                class EmailVerifyRecordAdmin(object):
                                    # 配置后台我们需要显示的列，如何在列表页中自定义显示某些列，
                                    list_display = ['code', 'email','send_type', 'send_time']
                                    
                                    # 配置搜索字段,不做时间搜索，页面进行查询
                                    search_fields =  ['code', 'email','send_type']
                                   
                                    # 配置筛选字段(过滤器)
                                    list_filter =  ['code', 'email','send_type', 'send_time']
                                   
                
                        
```