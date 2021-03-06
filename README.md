## django项目的应用模块导入问题
    在一个项目中创建多个应用时，单独放置显得文件太多，也不容易管理，所以一般都会创建一个apps
    文件夹，把创建的所有应用都放置进去，这时候，在settings.py文件中引入应用时就会报错，例如：
    ModuleNotFoundError: No module named 'users'，出错的主要原因是apps文件夹找不到，所以需
    要在settings.py文件中加入：
    import sys
    sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

    第二种解决办法就是在应用下面的apps.py里面，将原有的 name = 'users' 修改为  name = 'apps.users'
    
## 在上述问题解决之后，在创建模型的时候引入其他模型时，会有错误
    如果写成from apps.users.models import BaseModel就会报错：
    Model class apps.users.models.UserProfile doesn't declare an explicit app_label

    解决办法就是去掉apps. 直接写成from users.models import BaseModel即可

## django框架中使用xadmin的步骤
   1. 首先是下载对应版本的xadmin，然后解压放到项目根目录下，根据课程给予的
   xadmin配置的txt文件进行操作
   2. 然后下载的时候，避免使用单独下载太过麻烦，可以进入到xadmin目录下
   运行pip install requirements.txt 文件进行下载
   3. 下载完成以后，要在项目中进行配置，在项目的urls.py文件中配置，与django自带的admin后台管理配置相同
   4. 然后在每个应用下面新建一个xadmin.py进行配置，具体看代码
   5. 还有后台标题与脚部的文字定义，参考courses应用下的adminx.py文件中的GlobalSettings，主题参考BaseSettings
   6. GlobalSettings配置下的menu_style配置可已将侧边栏折起来

## xadmin的使用与django自带的admin类似
    先编写模块函数：
    class LessonAdmin(object):
        list_display = ['course', 'name', 'add_time']
        search_fields = ['course', 'name']
        list_filter = ['course__name', 'name', 'add_time']
    然后进行注册：
    xadmin.site.register(Lesson, LessonAdmin)

## 在xadmin中将模块功能或者表用中文显示的方法
   模块：在应用的apps.py中在class下使用： 
   verbose_name = "课程管理"
   表：在每个模块下：
   class Meta：
      verbose_name = "课程"

## 在使用xadmin时，对于外键的过滤的办法
   teacher__name 双下划线添加到list_filter数组里

## django路由的使用与模板渲染
   1. 路由注册：现在应用的views.py文件中定义路由函数
      例如，退出登录：
      class LogoutView(View): 函数里面写自己的逻辑
      然后在项目的urls模块中导入，进行注册：
      path('logout/', LogoutView.as_view(), name="logout"),
      name起的名字是为了在html中的href或者表单的action使用
      这样就可以维护的时候，只用修改后端，前端不用动
      html使用方法：
      href: href="{% url 'logout' %}"
      action同理

## 登录与退出功能中使用了django自带的函数login，logout
    from django.contrib.auth import authenticate, login, logout
    authenticate在登录想数据库查询用户名与密码时使用
## 登录校验功能是使用的django自带的表单验证
    使用方法：
    from django import forms
    class LoginForm(forms.Form):
        username = forms.CharField(required=True, min_length=2)
        password = forms.CharField(required=True, min_length=3)


## 短信验证使用的是云片网
   云片网使用需要先申请签名和模板，成功后才能使用
   签名申请的时候，如果没有域名，小程序审核也没有通过(就像我)
   这个时候，申请签名的时候就是用自己的真实姓名就可以了，什么都不选
   然后选择模板就好了

## 登录时图片验证码的引入与使用
   需要下载django-simple-captcha，可以参考网上文档进行使用
   这里是使用form的方式，在users应用下的forms.py中：
   class DynamicLoginForm(forms.Form):
    captcha = CaptchaField()
   然后在views.py的登录函数中，实例化，传给页面，在页面中{{ login_form.captcha }}
   就可以了
   点击图片可以进行验证码的刷新，这些逻辑，讲师已经写好了，在对应的js文件中

## 短信验证码的登录保存使用redis
    windows安装redis后，启用命令是：
    cd 到解压的文件夹下，打开cmd或者powershell窗口，使用redis-server.exe redis.windows.conf
    查看redis数据库数据，在启用redis服务后，再打开一个窗口，输入redis-cli.exe，就可以进入
    输入keys *就可以查看当前存储的键值对，输入flushdb就可以清空所有的键值对
    具体使用，自行百度

## 短信验证码动态登录
   发送短信的方法可以参考util下的YunPian.py，填写手机号，验证码点击就会发送短信，
   发送的短信验证码会被保存在redis里面，键值是手机号，值是随机验证码

## 前端页面中值回填的问题
   1. 如果动态登录表单填写出错的时候，我们希望之前填写的字段回填到页面上，这时，由于动态登录时，
   login_form绑定了一个实例化的DynamicLoginPostForm，没有办法绑定DynamicLoginForm，就会出现
   图片验证码刷新不了，所以又使用了d_form，但是二者不会同时出现
   2. 还有一个问题就是第一次进入动态登录的时候，可能因为获取不到值，这样就会回填None，为了避免
   这个问题可以使用 value="{{ login_form.mobile.value|default_if_none:'' }}" 需要注意的是
   | 和 default 还有 : 和 '' 之间不能有空格，否则会报错default_if_none需要两个参数，只传递了一个

## 将静态文件css和js的加载更改为django模板的样式
   首先在html标签下面添加 {% load staticfiles %} 引用的时候更改为 href="{% static 'css/reset.css' %}"
   这个也是有项目下面的settings.py文件里面的 STATIC_URL = '/static/' 配置有关，这样以后变更文件夹的话，
   就只用修改这个配置文件就可以了

## 对于html的渲染，我们需要使用基础模板，其他的继承基础模板的方法来用
   首先需要写一个基础模板，定义 {% block custom_css %} {% endblock %}
   这是为了让其他html继承基础模板的使用，知道插入哪一部分，使用方法和java中
   的thymeleaf模板引擎方法一样

## 在后台管理系统中添加的时候，上传图片后，项目目录下会生成一个图片文件夹
   比如说，课程机构的添加，上传图片的时候，就会生成一个org文件夹，这是因为
   在oranizations应用下的models.py中的CourseOrg下有一个：
   image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo", max_length=100)
   通过这个配置就能明白

## 因为需要上传的图片种类(课程，城市，老师)比较多，所以需要统一管理
   1. 在settings.py文件里，配置：
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   将生成的所有的上传文件统一保存到项目根目录下的media文件夹下
   2. 将配置好的路径传递到前端页面，方便显示，第一种方法是：
   在对应的views.py文件里面，引入settings.py定义的变量，通过render
   渲染页面的时候，携带参数传递给前端，但是这种方法操作起来，增加
   了代码的量，并且不易于维护，所以可以使用第二种方法：
   引入django自带的方法：在settings.py文件中的TEMPLATES的OPTIONS下
   添加：'django.template.context_processors.media' 这样就可以直接
   在前段页面中使用 MEDIA_URL，可以点击进入看一下源码，名字是相同的，
   不是随便起的

## ！！！只要是后期往模型里面添加字段，后面需要使用该字段的，就需要运行makemigrations 和 migrate命令，生成迁移，同步到数据库中

## 关于机构列表中经典课程的显示
   1. 我们可以再课程机构这个模型中引入课程，定义一个方法，在里面查询所有的课程进行返回
      这种方法使用要注意，引入course的时候，要在方法里面，如果在模型的最上方，就会出现
      循环导入的问题，因为在课程里面也导入了课程机构
   2. 可以通过django的高级语法，也就是如果一个对象是另一个对象的外键的时候，可以：
      def courses(self):
        courses = self.course_set.all()
        return courses

## 分页使用的是django-pure-pagination
   先试用pip安装，然后在settings.py中加入到INSTALLED_APPS

## 完成课程机构四个页面的显示，并且使每个应用都有自己的路由urls.py，然后在项目的urls.py包含进去
   在每个应用下使用urlpatterns=[] 去定义自己的路由，然后在项目
   urls.py中： url(r'^org/', include(('apps.organizations.urls', "organizations"), namespace="org")),
   将应用的路由包含进来

## 对于访问后台接口csrf_token的验证问题，解决办法有三种
   1. 在对应的form表单中添加{% csrf_token %}
   2. 在路由中使用url(r'^send_sms/', csrf_exempt(SendSmsView.as_view()), name="send_sms"),
      csrf_exempt去避免验证
   3. 如果是ajax请求访问：
      beforeSend: function (xhr, settings) {
         xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
      },
      这样让后台自己去随机生成一个，后台不用自己写代码

## 完成课程机构详情页面的展示
   对于详情页面的展示，需要传入对应的机构id，路由设计为：
   url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name="teacher"),
   前端页面通过超链接访问时：href="{% url 'org:course' course_org.id %}" 传入id

## 完成了收藏功能
   收藏功能首先要判断是否进行了登录，之后在进行验证，然后根据类型，进行判断保存

## 页面中显示图片的方式
   在settings.py中配置media处理器，页面中使用{{ MEDIA_URL }}{{ course.image }}
   还有就是直接{{ course.image.url }}

## 完成公开课程的显示、分页、排序(热门、人数)

## 完成课程详情，收藏功能，以及相关课程推荐
   相关课程推荐的完成有两种方法：
   1. 通过课程模型中的tag属性，然后使用django的模糊查询
   2. 再建一个CourseTag模型关联course，这样的话，一个课程就可以设置多个标签，分类明显
      并且易于管理维护
   推荐的时候注意要首先排除自身，然后要注意一门课程多个标签符合重复添加的问题，这个时候
   可以使用set，可以避免重复

## 课程中的难度在页面中显示的问题
   由于模型中 使用的是choices("zj", "初级")，这样数据库中保存的是zj，但是页面中要显示
   初级，所以前端页面中处理时，可以写成course.get_degree_display解决问题

## 完成资料下载，章节显示，视频播放，课程评论功能

## 完成讲师显示、分页、人气排名、排行榜、详情功能

## 完成了个人中心页面的显示，密码、手机号等个人信息的修改，头像上传修改功能，还有我的课程，收藏，消息等的显示

## 关于使用百度分享的问题
   使用这个功能时，有几个参数，尤其是bdUrl这个参数，这个参数要求的url值必须是已经存在的域名，不能是本机

## !!! 当一张表中的外键是另一张表时，另一张表的对象就可以通过反向的方法查询所有关联的内容
   比如：course-detail.html页面 学习用户的显示
   在usercourse表中有course的外键，所以可以直接通过course的对象直接反向查询所有的该课程的
   学习用户，也就是在usercourse表中查询学习该course的用户
   eg：前端页面可以直接循环course.usercourse_set.all就可以，如果我们不想要显示所有用户，也就是对
   查询结果进行截取，可以course.usercourse_set.all|slice:"3" 注意！！！一定要带""，否则
   会报int object has no 'split' attribute

## 实现自定义登录验证功能，让用户可以使用用户名或者手机号都可以进行登录
   首先要在users views.py文件中实现一个class CustomAuth然后在项目的settings.py中配置
   AUTHENTICATION_BACKENDS = [
    "apps.users.views.CustomAuth"
   ]
   这样用户在登录的时候，就会自动进入该类进行登录的判断

## 对于sql注入攻击的防范
   1. 可以通过form表单校验
   2. 自定义登录验证器，分多个层次进行校验，都通过后在进行后续操作
   3. 利用框架自身进行防范

## xadmin框架布局自定义
   通过在adminx.py中自定义，方法参考courses应用

## 如何让一个讲师对应一个用户，使讲师也能到登录到后台管理系统，但是讲师只能增删查改自己的课程
   1. 首先需要创建一个分组(讲师组)，该组的权限就是增删查改课程
   2. 把讲师添加到分组中
   3. 然后，改变之前的model模型，将teacher绑定用户，进行一对一绑定，具体参考代码
   4. 然后，在courses应用中的adminx.py中实现queryset方法，进行过滤，如果不是超级用户，
      那就是讲师，将当前讲师的课程过滤出来，相当于登录后台后只显示当前讲师的课程，当前讲师
      也只有对他课程的增删查改权限

## 如何在后台对一张表进行两个管理，也就是对一张表，后台侧边栏显示两个标签，管理的是同一张表
   比如说课程和轮播课程，都是课程表，但是轮播课程显示的只有is_banner为True的课程
   这样的话，可以添加一个类BannerCourse继承Course，然后在class Meta中配置的时候
   一定要加上proxy = True，这样就不会生成新的表，也就是对同一张表的管理

## 如何在后台管理中，将课程图片显示出来，如果不配置的话，默认显示的是图片地址
   首先我们需要在Course类下实现一个Show_image的方法，然后在adminx的list_display显示列中将方法名称配置进去
   然后我们应该给这一列配置一个名称，如果不配置的话，默认显示方法名称，
   配置方法在Course类下添加 show_image.short_description = "图片"

## 后台管理 只读字段还有看不到的字段配置都在adminx.py中
   只读：readonly_fields
   看不到：exclude
   但是只读和看不到不能同时配置相同字段(也就是在只读中或者看不到中配置的字段，就不能再看不到和只读中配置)
   注意：！！！对于必填的字段不要配置(有default值的除外)

## 配置后台管理中的图标
   xadmin自带的是font-awesome图标库，如果我们觉得版本太低的话，可以自行下载
   然后复制其中的css和fonts文件夹，覆盖项目中xadmin文件夹下static/vendor/font-awesome
   文件夹下的css和fonts文件夹就可以了
   使用的时候，复制类名，然后在adminx.py中进行配置

## 如果我们想要在添加课程的时候，把章节等的也进行添加，如何配置
   首先在adminx.py中实现一个类：
   class LessonInline(object):
      model = Lesson
      style = "tab"
      extra = 0
      exclude = ["add_time"]
   其他的也是模仿这样，比如：
   class CourseResourceInline(object):
      model = CourseResource
      style = "tab"
      extra = 1
   然后再在想要配置的类中添加inlines：
   inlines = [LessonInline, CourseResourceInline] (我们这里是配置课程)
   其他的类似

## 上述配置中的inlines属性的bug
   不能在inlines中两个类中同时使用tab，暂时不能解决

## 在adminx.py中配置布局与exclude看不到的问题
   两者不能同时配置，否则会冲突，也就是在布局中显示的字段，exclude中
   不要配置，一个显示，一个不显示，会冲突

## django项目中继承Ueditor插件
   1. 将djangoueditor源码拷贝到项目根目录下
   2. INSTALLED_APPS 中配置 'DjangoUeditor'
   3. 配置相关的url，在项目urls.py中:
      url(r'^ueditor/',include('DjangoUeditor.urls')),
   4. 下载ueditor插件并放置到xadmin源码的plugins目录下
   5. 将editor文件名配置到plugins目录下的__init__.py文件的PLUGINS变量中
   6. 在对应的model的管理器中配置，也就是adminx.py文件中：
      style_fields = {
         "detail":"ueditor"
      }
      detail表示model中富文本的字段
   此外，还要将原来的模型中想要用富文本的字段改为使用UEditorField定义
   注意，富文本编辑器保存的是一段html代码，如果想要在前端页面中正常显示
   需要这样写：{% autoescape off %}{{ course.detail }}{% endautoescape %}

## 实现导入导出功能
   默认的导出功能也是可以的，但是我们想要自己勾选进行导出，或者导入已有数据到项目中，默认的是满足不了的，自己实现
   首先要在settings.py中INSTALLED_APPS进行注入import_export

   然后在adminx.py中，先导入from import_export import resources
   然后实现一个类：
   class MyResource(resources.ModelResource):
      class Meta:
         model = Course
   然后在你想要使用此功能的类里面，这里我们指定的是Course，加入
   import_export_args = {'import_resource_class': MyResource, 'export_resource_class': MyResource}

   这个时候，由于项目自带的有一个导出功能，所以页面上会显示两个导出
   如果想要把项目自带的注销，就可以在xadmin/plugin下面的__init__.py
   文件中将export注释即可
   其他的想要使用导入导出，配置类似
   