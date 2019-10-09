from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=3, label="用户名",
                               widget=forms.TextInput(attrs={
                                   "class": ""
                               })
                               )

    password = forms.CharField(max_length=30, min_length=6, label="密码",
                               widget=forms.PasswordInput(attrs={
                                   "class": ""
                               })
                               )

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        usr = auth.authenticate(username=username, password=password)

        if usr is None:
            raise forms.ValidationError('用户名或密码不正确{}{}'.format(username,password))
        else:
            self.cleaned_data["usr"] = usr
        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=3, label="用户名",
                               widget=forms.TextInput(attrs={
                                   "class": "",
                                   "placeholder": "请输入用户名，长度3~20",
                               })
                               )

    email = forms.EmailField(max_length=20, min_length=3, label="邮件",
                               widget=forms.EmailInput(attrs={
                                   "class": "",
                                   "placeholder": "请输入用户名，长度3~20",
                               })
                               )

    password = forms.CharField(max_length=30, min_length=6, label="密码",
                               widget=forms.PasswordInput(attrs={
                                   "class": "",
                                   "placeholder": "请输入密码，长度6~20",
                               })
                               )

    reconfirm_password = forms.CharField(max_length=30, min_length=6, label="再次输入密码",
                               widget=forms.PasswordInput(attrs={
                                   "class": "",
                                   "placeholder": "请再次输入密码，长度6~20",
                               })
                               )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username):
            raise forms.ValidationError("用户名已经存在")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email):
            raise forms.ValidationError("email已经存在")
        return email

    def clean_reconfirm_password(self):
        password = self.cleaned_data['password']
        reconfirm_password = self.cleaned_data['reconfirm_password']
        if password != reconfirm_password:
            raise forms.ValidationError("两次输入的密码不一样")
        return reconfirm_password
