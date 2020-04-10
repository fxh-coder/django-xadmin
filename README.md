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
