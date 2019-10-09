from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType

from .models import LikeCount, LikeRecord

# Create your views here.
def likes_change(request):
    content_type = request.GET.get("content_type")
    object_id = request.GET.get("object_id")
    is_likes = request.GET.get("is_likes")
    usr = request.user

    if not usr.is_authenticated:
        # 没有授权，显示错误
        pass

    if ContentType.objects.filter(content_type=content_type, object_id=object_id).exists():
        content_object = ContentType.objects.get(content_type=content_type, object_id=object_id)
    else:
        pass

    if is_likes:
        # 已经点赞
        pass
    else:
        # 没有点赞
        pass



    pass