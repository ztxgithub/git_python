# Django 基础知识

## 基本技巧

```shell
    1. views.py 内容中
            from .models import UserMessage ---> 这里 "." 代表和 views.py 文件同一层级下 models.py
                + views.py
                + models.py
                
    2. 如果在 *.py 中有中文出现，则在头部一定要写上 
            # coding:utf-8
            
    3. 在 *.html 中所有表单提交的时候都要加 {% csrf_token %}
    4. 在数据库的一对多(一个课程对应多个章节)，可以用 Django 的外键
    5. MTV 模式：M(model), T(template), V(view), template 即 HTML 模板，页面展示的 HTML 代码
       当用户输入一个 URL 时，该 URL 找到相应的视图(views.py)，执行视图的某部分，如需查询数据库，则会使用数据库模型获取数据，
       在视图程序中通过指定的HTML文件，以页面的形式显示给用户
```

## ORM 操作

```shell
    1. 在 models.py 中添加相应的数据库类
        class UserMessage(models.Model):
            """
                name 字段的最大长度
                verbose_name 代表该字段的注释 u"用户名": Unicode编码
            """
            name = models.CharField(max_length=20, verbose_name= u"用户名")
            email = models.EmailField(verbose_name=u"邮箱")
            address = models.CharField(max_length=100, verbose_name= u"地址")
            message = models.CharField(max_length=500, verbose_name= u"留言信息")
        
            class Meta:
                verbose_name = u"用户留言信息"
                
         注意：
            因为代码中加了中文，在文件的开头加入 # coding: utf-8
                
    2. 每建一个 app 需要在 settings.py 进行注册
             INSTALLED_APPS = [
                'message'
            ]
                
    3. 在 PyCharm 中 Tools->Run manager.py Task,主要是通过以下的命令对
       数据库表进行变更
            manage.py@untitled1 > makemigrations message(这个是 apps 名字)
            manage.py@DjangoGetStarted > migrate message
            
    4. 当 models.py 中代码有修改需要同步到数据库
            manage.py@untitled1 > makemigrations courses(这个是 apps 名字)
            manage.py@DjangoGetStarted > migrate courses
            
            问题一: 在进行 makemigrations message 时出现 ValueError: too many values to unpack
            原因是： apps/courses/migrations/0001_initial.py 中 
                    ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.courses.Course', 
                                                 verbose_name='\u8bfe\u7a0b')),
                                                 
                    to='apps.courses.Course'
                    
            修改:
                    to='apps.courses.Course' 改为 to='.courses.Course'
            
```

## models.py 数据类型

```shell
    1. model.py 相关的知识点
    
        models.ForeignKey     : 对应于数据库的外键
        models.DateTimeField  : 对应于数据库的日期
        models.IntegerField   : 对应于数据库的整型  
        models.IPAddressField : 对应 IP 地址类型
        models.FileField      : 用于上传文件类型
            download = models.FileField(
                                        upload_to="course/resource/%Y/%m",
                                        verbose_name=u"资源文件",
                                        max_length=100)
        models.ImageField     : 用于图片类型
             # 头像图片, 图片可以上传到某个目录，也可以有默认图片
             image = models.ImageField(upload_to="image/%T/%m", 
                                       default=u"image/default.png", 
                                       max_length=100)
        models.CharField:
                参数:
                    (1) max_length : 最大字符长度
                    (2) null = True, blank=True : 该字段可以为空
                    (3) default=""  设定默认值为空
                    
        models.TextField: 允许不输入最大长度
              detail = models.TextField(verbose_name=u"课程详情")
              
        models.ForeignKey：外键
            class Lesson(models.Model):
                    course = models.ForeignKey(Course, verbose_name=u"课程")
                    因为一个课程对应很多章节。所以在章节表中将课程设置为外键，
                    作为一个字段来让我们可以知道这个章节对应那个课程
                    
        models.BooleanField:
                has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
                    
        (1).自己定义主键：
            object_id(字段名) = models.CharField(primary_key=True, max_length=50,
                                                default="", verbose_name="主键")
                                                
        (2). 指定表名
                db_table = "表名"
                
        (3).数据库中定义可见的选择(使用 choices)，例如性别
            gender = models.CharField(choices=(("male", u"男"), ("female", u"女")), 
                                      default="male")
                                      
        (4) 在 model.py 自定义类中，需要重载 Unicode方法, 否则在 print UserProfile 实例的时候
            就不能打印我们自定义的字符串，打印实例会打印username，username为继承自abstractuser
                class UserProfile(AbstractUser):
                     # 昵称
                        nick_name = models.CharField(max_length=50, 
                                                     verbose_name=u"昵称", 
                                                     default="")
                        def __unicode__(self):
                              return self.username     
                              
        (5)  在 model.py 自定义类中当前记录的生成时间 
                time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")    
                其中now得去掉(), datetime.now() 是根据编译时间， datetime.now是根据实例化时间   
                
                                
                     
                                      
        
            
                
    2. 在 views.py 中引入数据库类
            from .models import UserMessage
           
         (1). # UserMessage默认的数据管理器objects
            # 方法1 :all()是将所有数据返回成一个queryset类型(django的内置类型)
            # all_message = UserMessage.objects.all()
            
            # 我们可以对于all_message进行遍历操作
            # for message in all_message:
            #     message.delete()
            #     # 每个message实际就是一个UserMessage对象（这时我们就可以使用对象的相关方法）。
            #     print message.name
            
         (2).  根据条件对数据库进行筛选
             filter取出指定条件值，逗号代表and 必须同时满足两个条件才返回。
             all_message = UserMessage.objects.filter(name='mtianyan', address='西安')
            
         (3).  将数据保存到数据库中

               (1) 首先实例化一个对象
                     user_message = UserMessage()
        
               (2) 为对象增加属性
                     user_message.name = "mtianyan2"
                     user_message.message = "blog.mtianyan.cn"
                     user_message.address = "西安"
                     user_message.email = "1147727180@qq.com"
                     user_message.object_id = "efgh"
        
                (3) 调用save方法进行保存
                     user_message.save()
                     
         (4). 在网页上填写信息，post 提交给后台，后台再存数据库
                def getform(request):
                    # html表单部分
                
                    # 此处对应html中的method="post"，表示我们只处理post请求
                      if request.method == "POST":
                       # 就是取字典里key对应value值而已。取name，取不到默认空
                       ```
                         这里的 key 一定要和 message_from.html 中的 name 的值对应起来
                        <input id="name" type="text" name="name"  value="{% ifequal my_message.name|slice:"8" "mtianyan1"|slice:"8" %}
                            对应中文昵称：天涯明月笙 {% else %} 未找到中文昵称
                        ```
        
                        name = request.POST.get('name', '')  
                        message = request.POST.get('message', '')
                        address = request.POST.get('address', '')
                        email = request.POST.get('email', '')
                    
                         # 实例化对象
                         user_message = UserMessage()
                    
                        # 将html的值传入我们实例化的对象.
                         user_message.name = name
                         user_message.message = message
                         user_message.address = address
                         user_message.email = email
                         user_message.object_id = "ijkl"
                    
                         # 调用save方法进行保存
                         user_message.save()
                
                    return render(request, 'message_form.html',{
                        "my_message" : message
                    })
                    
         (5). 数据的删除
                all_message = UserMessage.objects.filter(name='mtianyan', address='西安')
                all_message.delete() # 将所有符合条件的删除
                
                for message in all_message:
                      message.delete()  # 对记录进行删除

        
    3. 从后台读数据，在前端显示
            (1) 在 views.py 中
                    # 引用数据库 Model 类型
                    from .models import UserMessage
                    
                    def getform(request):
                          message = None
                            all_message = UserMessage.objects.filter(name='mtianyan', address='西安')
                        
                            # if 判断是否存在数据
                            if all_message:
                                # all_message是一个list，可以使用切片。
                                message = all_message[0]
                          
                          # 对应于 message_form.html 页面，其中在 message_form.html 中  
                          # my_message 变量等同于 message
                          return render(request, 'message_form.html',{
                                "my_message" : message
                            })
                            
            (2) 在 message_form.html 页面中
            
                   A. 对于 input 标签
                        <input id="email" type="email" value="{{ my_message.email}}" 
                        name="email" placeholder="请输入邮箱地址"/>
                    
                    其中 value 为 my_message.email，则显示从 views.py 中 render 出来的值
                    
                   B. 对于 textarea
                        <textarea id="message" name="message"  placeholder="请输入你的建议">
                        {{ my_message.message }}
                        </textarea>
                        
                        
            (3) Django template(html) 中限制了很多 python 逻辑，如果想用 if else 逻辑只能有 Django 特定的
            
                   A. if else 用法
                    <input id="email" type="email" value="{% if my_message.name == 'bobbytest'%}bobbytest
                    {% else %} boobyno{%endif%}" 
                        name="email" placeholder="请输入邮箱地址"/>
                        
                        含义是如果 my_message.name 为 bobbytest, 则输出 bobbytest,否则输出 boobyno
                    
                   B. ifequal
                         <input id="email" type="email" value="{% ifequal my_message.name 'bobbytest' %}bobbytest
                    {% else %} boobyno{% endifequal %}" 
                        name="email" placeholder="请输入邮箱地址"/>
                        
                        含义是如果 my_message.name 为 bobbytest, 则输出 bobbytest,否则输出 boobyno
                        
                   C. 取前五个字符 |slice:'5'
                   
                        <input id="email" type="email" value="{% ifequal my_message.name|slice:'5' 'bobbytest' %}bobbytest
                    {% else %} boobyno{% endifequal %}" 
                        name="email" placeholder="请输入邮箱地址"/>
                        
    4. 浏览器访问 http://127.0.0.1:8000/form/ 对应的页面
            (1) 在 urls.py 中
                    urlpatterns = [
                        url(r'^admin/', admin.site.urls),
                        url(r'^form/$', getform, name="form_new"),
                    ]
                    
                    访问 http://127.0.0.1:8000/form/ 会调用 views.py 中 getform函数，getform函数中
                    有 render() 函数 会跳转到对应的页面 message_form.html， 而 message_form.html 中
                    <form action="{% url "form_new" %}" method="post" class="smart-green"> 中
                    action 将 url 赋值为 form_new (从 urls.py 中取)，所以以后你如果想要修改对应的
                    url 但页面不变，则需要 改 url(r'^form/$', getform, name="form_new") 中 
                    r'^form/$ 就行了
                    
                    A. 在 urlpatterns 中 url 匹配的先后顺序
                            urlpatterns = [
                        url(r'^admin/', admin.site.urls),
                        url(r'^form', getform, name="form_new"),
                        url(r'^formtest', admin.site.urls),
                    ]
                    
                    如果页面访问 http://127.0.0.1:8000/formtest  则会跳转到 getform 页面，而不是 admin.site.urls , 
                    因为正则匹配到了  url(r'^form', getform, name="form_new") ， 正确写法是
                                   url(r'^form/$', getform, name="form_new") 
                    
                    
        
```