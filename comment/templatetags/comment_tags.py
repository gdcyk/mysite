from django import template
from django.contrib.contenttypes.models import ContentType

from blog.models import Blog
from comment.models import Comment
from comment.forms import CommentForm

register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    ct = ContentType.objects.get_for_model(obj)  # 使用的是blog的模型
    return Comment.objects.filter(content_type=ct, object_id=obj.pk).count()

@register.simple_tag
def get_comment_form(blog_pk, obj):
    initial = {
        "object_id": blog_pk,
        "content_type": ContentType.objects.get_for_model(obj).model,
        "reply_comment_id": 0
    }
    comment_form = CommentForm(initial=initial)
    return comment_form

@register.simple_tag
def get_comments(obj):
    ct = ContentType.objects.get_for_model(obj)  # 使用的是blog的模型
    comments = Comment.objects.filter(content_type=ct, object_id=obj.pk, parent=None).order_by("-comment_time")
    return comments

from django.utils.safestring import mark_safe
@register.simple_tag
def my_input():
    result = "<div>你们好,我是开发者</div>"
    return mark_safe(result)