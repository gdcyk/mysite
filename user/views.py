from django.shortcuts import render, redirect,reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse

from user.forms import LoginForm, RegisterForm

# Create your views here.
def login(request):
    """
    Login界面提交信息，或者从别的地方进入login页面
    1、POST就是Login界面提交信息，action为“”空，POST自身，然后重定位进入页面
    2、否则就是从别的页面进入，显示要输入的信息
    :param request:
    :return:
    """
    if request.method == "POST":
        login_forms = LoginForm(request.POST)
        if login_forms.is_valid():
            usr = login_forms.cleaned_data["usr"]
            auth.login(request, usr)
            print(request.GET.get("from", reverse("home")))
            return redirect(request.GET.get("from", reverse("home")))
    else:
        login_forms = LoginForm()
    context = {}
    context['login_forms'] = login_forms
    return render(request, "login.html", context=context)

def login_for_modal(request):
    login_forms = LoginForm(request.POST)
    data = {}
    if login_forms.is_valid():
        usr = login_forms.cleaned_data["usr"]
        auth.login(request, usr)
        print(request.GET.get("from", reverse("home")))
        data["status"] = "SUCCESS"
    else:
        data["status"] = "ERROR"
    return JsonResponse(data)

def register(request):
    if request.method == "POST":
        register_forms = RegisterForm(request.POST)
        if register_forms.is_valid():
            usr = User()
            usr.username = register_forms.cleaned_data["username"]
            usr.email = register_forms.cleaned_data["email"]
            # 只能使用set_password，因为要加密
            usr.set_password(register_forms.cleaned_data["password"])
            usr.save()
            print(usr.username, usr.email, usr.password)
            auth.login(request, usr)
            print(request.GET.get("from", reverse("home")))
            return redirect(request.GET.get("from", reverse("home")))
    else:
        register_forms = RegisterForm()
    context = {}
    context['register_forms'] = register_forms
    return render(request, "register.html", context=context)

def logout(request):
    user = request.user
    if user.is_authenticated:
        auth.logout(request=request)
    referer = request.META.get("HTTP_REFERER", "home")
    print(referer)
    return redirect(referer)

def user_info(request):
    return render(request, "user_info.html", context=None)