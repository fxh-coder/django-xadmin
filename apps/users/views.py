from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, RegisterPostForm
from utils.YunPian import send_single_sms
from utils.random_str import generate_random
from MxOnline.settings import yp_apikey, REDIS_HOST, REDIS_PORT
import redis
from users.models import UserProfile


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, "register.html", {
            "register_get_form": register_get_form
        })

    def post(self, request, *args, **kwargs):
        print("post")
        register_post_form = RegisterPostForm(request.POST)
        # 这个字段是为了错误的话返回的仍然是动态登录的tab，会在前段页面中进行判断
        if register_post_form.is_valid():
            # 没有注册账号依然可以登录
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            # 新建一个用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterGetForm()
            return render(request, "register.html", {
                "register_get_form": register_get_form,
                "register_post_form": register_post_form
            })


class DynamicLoginView(View):
    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        # 这个字段是为了错误的话返回的仍然是动态登录的tab，会在前段页面中进行判断
        dynamic_login = True
        if login_form.is_valid():
            # 没有注册账号依然可以登录
            mobile = login_form.cleaned_data["mobile"]
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                # 新建一个用户
                user = UserProfile(username=mobile)
                password = generate_random(10, 2)
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            d_form = DynamicLoginForm()
            return render(request, "login.html", {"login_form": login_form,
                                                  "d_form": d_form,
                                                  "dynamic_login": dynamic_login})


class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            # 随机生成验证码
            code = generate_random(4, 0)
            re_json = send_single_sms(yp_apikey, code, mobile=mobile)

            if re_json["code"] == 0:
                re_dict["status"] = "success"
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                                db=0, charset="utf8", decode_responses=True)
                r.set(str(mobile), code)
                r.expire(str(mobile), 60*5)
            else:
                re_dict["msg"] = re_json["msg"]
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]

        return JsonResponse(re_dict)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        login_form = DynamicLoginForm()
        return render(request, "login.html", {
            "login_form": login_form
        })

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]

            user = authenticate(username=user_name, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})
