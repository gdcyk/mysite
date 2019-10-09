from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget

from .models import Comment

class CommentForm(forms.Form):
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type = forms.CharField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name="comment_ckeditor"),
                           error_messages={"required":"评论不能为空"})
    # 因为是hidden，看不见，添加id为reply_comment_id
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={"id": "reply_comment_id"}))

    def __init__(self, *args, **kwargs):
        if "user" in kwargs:
            self.user = kwargs.pop("user")
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data["user"] = self.user
        else:
            raise forms.ValidationError("未登录，请登录")
        print("user")
        object_id = self.cleaned_data["object_id"]
        content_type = self.cleaned_data["content_type"]
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_object = model_class.objects.get(pk=object_id)
            self.cleaned_data["model_object"] = model_object
        except ObjectDoesNotExist:
            raise forms.ValidationError(("评论对象不存在"))

        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data["reply_comment_id"]
        if reply_comment_id<0:
            raise forms.ValidationError("评论目标id不合法")
        elif reply_comment_id == 0:
            self.cleaned_data["parent"] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data["parent"] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError("回复出错")
        return reply_comment_id