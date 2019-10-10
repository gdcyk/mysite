from django.template import Library
from django.contrib.contenttypes.models import ContentType
from likes.views import LikeCount, LikeRecord

register = Library()

@register.simple_tag
def get_like_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=ct, object_id=obj.pk)
    return like_count.likes_num

@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    user = context["user"]
    if user.is_authenticated:
        ct = ContentType.objects.get_for_model(obj)
        if LikeRecord.objects.filter(content_type=ct, object_id=obj.pk, user=user).exists():
            return "active"
    return ""
