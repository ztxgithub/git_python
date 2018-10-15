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
    
    4. operation-用户操作管理（避免循环引用而采取的分层）
           主要用于记录用户的操作信息，比如 users 和 courses 之间的联系， users 和 organization 之间的联系
           
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
            
```