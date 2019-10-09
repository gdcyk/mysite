from django.shortcuts import render, redirect,reverse
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

from .models import Comment
from mysite.forms import LoginForm, RegisterForm
from comment.forms import CommentForm


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

# 按评论按钮后的操作
def update_comment(request):
    referer = request.META.get("HTTP_REFERER", "home")
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data["user"]
        comment.content_object = comment_form.cleaned_data["model_object"]
        comment.text = comment_form.cleaned_data["text"]

        # 添加root parent reply_to
        parent = comment_form.cleaned_data["parent"]
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        data["status"] = "SUCCESS"
        data["username"] = comment.user.username
        data["comment_time"] = comment.comment_time.strftime("%Y-%m-%d %H:%M:%S")
        data["text"] = comment.text
        if parent is not None:
            data["reply_to"] = comment.reply_to.username
        else:
            data["reply_to"] = ""
        data["pk"] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
        print("data['root_pk']:{}".format(data['root_pk']))
    else:
        data["status"] = "ERROR"
        data["message"] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)