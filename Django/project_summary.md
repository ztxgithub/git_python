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
                        
          
          
```