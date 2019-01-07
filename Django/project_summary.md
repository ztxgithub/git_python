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
                       (1). 在 apps/users/ 目录下新建 adminx.py (xadmin 会自动查找 apps 下 adminx.py,
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
                                (A) class EmailVerifyRecordAdmin(object):
                                        # 配置后台我们需要显示的列，如何在列表页中自定义显示某些列，
                                        list_display = ['code', 'email','send_type', 'send_time']
                                        
                                        # 配置搜索字段,不做时间搜索，页面进行查询
                                        search_fields =  ['code', 'email','send_type']
                                       
                                        # 配置筛选字段(过滤器)
                                        list_filter =  ['code', 'email','send_type', 'send_time']
                                    
                                (B) 如果要在配置筛选字段中过滤外键相关的字段 course(外键名) + "__" + 该外键类对应的字段名
                                        class LessonAdmin(object):
                                                # __name代表使用外键中name字段
                                                list_filter = ['course__name', 'name', 'add_time']
                                                
                                (C) 在 搜索字段 字段(search_fields),最好不要包含时间，不然会出错
                                
                       (6) 设置全局配置
                                (A) 
                                       # x admin 全局配置参数信息设置
                                        class GlobalSettings(object):
                                            # 在 http://127.0.0.1:8000/xadmin/ 页面中，左上角 "Django Xadmin"
                                            # 改为其他字符串
                                            site_title = "天涯明月笙: 慕课后台管理站"
                                            
                                            # 在 http://127.0.0.1:8000/xadmin/ 页面的底部 "© 我的公司" 改为其他的
                                            # 字符串
                                            site_footer = "mtianyan's mooc"
                                            
                                            # 在 http://127.0.0.1:8000/xadmin/ 页面的左边的导航栏设置为收缩模式
                                            # 收起菜单
                                            menu_style = "accordion"
                                            
                                        # 将头部与脚部信息进行注册:
                                         xadmin.site.register(views.CommAdminView, GlobalSettings)
                                
                                    
                                (B) 
                                    
                                (C) xadmin 的主题修改
                                        (1) 暂时在 users/adminx.py 中编辑
                                                from xadmin import views
                                                # 创建X admin的全局管理器并与view绑定。
                                                class BaseSetting(object):
                                                    # 开启主题功能
                                                    enable_themes = True
                                                    use_bootswatch = True
                                                    
                                                # 将全局配置管理与view绑定注册
                                                xadmin.site.register(views.BaseAdminView, BaseSetting)
                                                
                                        (2) 这时候在 http://127.0.0.1:8000/xadmin/ 页面的头部会出现 "主题"
                                
                                (D) 在 http://127.0.0.1:8000/xadmin/ 页面的左边栏 app 的名称(例如 COURSES 改为中文)
                                    (I)
                                        在 users/apps.py 中 加一个 verbose_name
                                                class UsersConfig(AppConfig):
                                                       name = 'users'
                                                        verbose_name = u"用户信息"
                                                        
                                    (II) 在 users/__init__.py 中加入
                                                # encoding: utf-8
                                                # 添加默认的app_config使app中文名生效
                                                default_app_config = "users.apps.UsersConfig"
                                                     
```

## 用户的登录和注册,找回密码

```shell

    1. 基础知识
            (1) 在通过网页 post 的 username 和　password 值，可以通过 Django 自带的 authenticate() 方法进行验证，其内部的实现是
                向对应的数据库查询是否有对应的用户名和密码
                    from django.contrib.auth import authenticate
                    # 成功返回user对象,失败返回null
                    user = authenticate(username = user_name, password = pass_word)
            (2) 拿到 username 和 password 后，调用 Django 自带的 login(request, user) 方法完成登录，其内部的实现是
                将传入参数中 request 对象的部分值进行赋值操作，之后通过 render(request, "index.html") 将这些信息待会给
                浏览器
                    from django.contrib.auth import login
                        login(request, user)
                        return render(request, "index.html") # 一般登录成功之后会跳转到首页或则个人中心页面
                        
                更为深层的原理是根据用户名和密码生成 session_id (针对服务端而言), 其保存在数据库中(django_session), 这个表
                存储了 Django 给每一个用户生成了 session 的信息(会对用户信息进行加密)，其中 session_key 字段实际上是服务器给
                用户(浏览器的 id ), session_data 字段是一段加密的字符串，把用户的信息(比如名称，密码等等)进行加密， 
                expire_date 过期时间
                        
            (3) 在用户登录业务中，可以通过邮箱和用户名两种方式进行登录，通过自定义 auth 方法，
                    第一步: 在 settings.py 添加
                                # 设置邮箱和用户名均可登录
                                    AUTHENTICATION_BACKENDS = (
                                        'users.views.CustomBackend',
                                    
                                    )
                    第二步: 在 users/viewer.py 中定义类 CustomBackend：
                                class CustomBackend(ModelBackend)：
                                        def authenticate(self, username=None, password=None, **kwargs):
                                            try:
                                                # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
                                                user = UserProfile.objects.get(Q(username=username)|Q(email=username))
                                                # django的后台中密码加密：所以不能password==password
                                                # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
                                                if user.check_password(password):
                                                    return user
                                            except Exception as e:
                                                return None
                                                
                    业务流程： 先调用 django.contrib.auth 中的 authenticate(username = user_name, password = pass_word)， 
                             之后这个方法会跳转到自己定义类 CustomBackend 的   
                             authenticate(self, username=None, password=None, **kwargs) 方法
                             
            (4) Django 中并集操作，from django.db.models import Q
                    Q(username=username)|Q(email=username)
            (5) 后台的值传到前端页面中, 例如将 views.py 中  return render(request, "login.html", {"msg":"用户名或密码错误! "})
                那么在 login.html 中将 msg 的值进行显示，
                     <div class="error btns login-form-tips" id="jsLoginTips">{{ msg }}</div>
            (6) 使用 Django form 进行表单预处理，例如 post 过来的字段进行判断以及限定条件，通过 form 进行事先处理而不是
                在自己的 class LoginView() 的 post 方法进行处理
                    第一步：在 users 创建 forms.py 文件
                                # 引入Django表单
                                from  django import forms
                                
                                # 登录表单验证
                                class LoginForm(forms.Form):
                                    # 用户名密码不能为空,如果为空会报错
                                    username = forms.CharField(required=True)
                                    # 密码不能小于5位
                                    password = forms.CharField(required=True, min_length=5)
                                    
                    第二步: 在 class LoginView() 的 post 方法创建 LoginForm 对象
                                    def post(self, request):
                                    # 类实例化需要一个字典参数dict: request.POST就是一个QueryDict所以直接传入
                                    # POST中的username,password，会对应到form中
                                    login_form = LoginForm(request.POST)
                            
                                    # is_valid判断我们字段是否有错,执行我们原有逻辑，验证失败跳回login页面
                                    if login_form.is_valid():
                                        ...........
                                    # 验证不成功跳回登录页面
                                    # 没有成功说明里面的值是None，并再次跳转回主页面
                                    else:
                                        return render(
                                            request, "login.html", {
                                                "login_form": login_form })
                                                
                           注意:
                                在 login.html 中
                                <input name="username" id="account_l" type="text" placeholder="手机号/邮箱" /> username 
                                必须与 class LoginForm() 中 username 字段一致.
                                
                    A. 将  login_form = LoginForm(request.POST) 中的 login_form 表单的信息显示给网站，在 login.html 中
                            <div class="form-group marb20 {% if login_form.errors.username %}errorput{% endif %} ">
                                    <label>用&nbsp;户&nbsp;名</label>
                                    <input name="username" id="account_l" type="text" placeholder="手机号/邮箱" />
                            </div>
                            在 div 中加入 {% if login_form.errors.username %}errorput{% endif %}, 这是 template 
                            语法，如果 login_form 中的 errors 中有 username 相关的错误信息，会 通过 errorput 显示高亮
                            
                            同时将错误信息打印，template 进行 for 循环，
                            {% for key, error in login_form.errors.items %} # for 开始
                            {{ error }}   # 遍历后的输出
                            {% endfor %}  # for 结束
                            
            (7) cookies
                    cookies 就是
                            
                            
    2.用户登录功能
            (1) 首页是 index.html , 将 index.html 放到项目的 templates 目录下
            (2) 在项目目录中右键新建 static ,用来存放 css, js, image 等静态文件
            (3) 在 project_dir(例如 custom_mxonline)/urls.py 中处理静态文件, index 页面的放回
                         ## 处理的文件是静态文件
                        from django.views.generic import TemplateView  
                            urlpatterns = [
                                             url('^$', TemplateView.as_view(template_name="index.html"), "index"),
                                          ]
                                          
                        在 settings.py 中指明 static 文件存放的路径
                            STATICFILES_DIRS = (
                                                    os.path.join(BASE_DIR, "static"),
                                                )
                        
                        在 index.html 中修改跟 static 相关的路径
                         将 <link rel="stylesheet" type="text/css" href="../css/reset.css">
                         修改为：
                            <link rel="stylesheet" type="text/css" href="{% static 'css/reset.css' %}">
                            
            (4) 
                a. 拷贝 login.html ，并且在资源路径中将类似 ../css/reset.css 替换为 {% static 'css/reset.css' %},
                b. 同时在 project_dir(例如 custom_mxonline)/urls.py 中加入 url
                   url('^login/$', TemplateView.as_view(template_name="login.html"), name = "login"),
                c. 在 index.html 中的"登录" 对应的 href 改为 "/login/"
                        <a style="color:white" class="fr loginbtn" href="/login/">登录</a>
                    
            (5) 编写后台逻辑
                    A. 登录基于函数
                                在 apps/users/views.py
                                    # 当我们配置url被这个view处理时，自动传入request对象.
                                    def user_login(request):
                                        # 前端向后端发送的请求方式: get 或post
                                        # 登录提交表单为post
                                        if request.method == "POST":
                                            .......
                                        # 获取登录页面为get
                                        elif request.method == "GET": 
                                            # render就是渲染html返回用户
                                            # render三变量: 第一个参数：request 
                                                           第二个参数：模板名称（html页面）
                                                           第三个参数：一个字典传给前端的值
                                            return render(request, "login.html", {})  
                                            
                            在 views.py 的 user_login 函数写好后，与之对应的是 urls.py
                                    from users.views import user_login
                                    urlpatterns = [
                                                    url('^login/$', user_login, name = "login"),
                                                  ]
                                                  
                            在 login.html 中进行账号登录时 <form action="/login/" method="post" autocomplete="off">..</from>
                            其中 action 对应的是 urls.py 中 url 的地址。
                            
                            如果在账号登录时进行 post 提交表单(form) 遇到“禁止访问403， csrf 验证失败，相应中断”，这是 Django 的安全机制，
                            Django 为了防止跨域的提交，刚开始向前端传递一个随机符号，在 post 的时候只有把这个随机符号带回去。
                            解决方法：加入 csrf_token,会自动生成 csrf_token 
                                <form ....>
                                {% csrf_token %}
                                </form>
                            
                            这个时候 F12 在 <form> 表单中出现
                             <input type="hidden" name="csrfmiddlewaretoken" value="ZSiXE7ay2FbP9ibHr6oePOlLi85zyiR7"> 
                             
                    B. 基于类方法实现登录(在 Django 中推荐使用基于类的方式)
                            (1) 在 users/views.py 中
                                    # 基于类实现需要继承的view
                                    from django.views.generic.base import View
                                    class LoginView(View):
                                        # 直接调用get方法免去判断
                                        def get(self, request):
                                            # render就是渲染html返回用户
                                            # render三变量: request 模板名称 一个字典写明传给前端的值
                                            return render(request, "login.html", {})
                                    
                                        def post(self, request):
                                            # 取不到时为空，username，password为前端页面name值
                                            user_name = request.POST.get("username", "")
                                            pass_word = request.POST.get("password", "")
                                
                                            # 成功返回user对象,失败返回null
                                            user = authenticate(username=user_name, password=pass_word)
                                
                                            # 如果不是null说明验证成功
                                            if user is not None:
                                                # login_in 两参数：request, user
                                                # 实际是对request写了一部分东西进去，然后在render的时候：
                                                # request是要render回去的。这些信息也就随着返回浏览器。完成登录
                                                login(request, user)
                                                # 跳转到首页 user request会被带回到首页
                                                return render(request, "index.html")
                                            # 仅当用户真的密码出错时
                                            else:
                                                return render(request, "login.html",{"msg":"用户名或密码错误!"})
                                            
                            (2) 在 project_dir/urls.py 中
                                    # 换用类实现
                                    from users.views import LoginView
                                    urlpatterns = [   
                                        # 基于类方法实现登录,这里是调用它的方法
                                        url('^login/$', LoginView.as_view(), name="login")
                                    ]
                                       
                
                    
```