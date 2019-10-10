from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist

from .models import LikeCount, LikeRecord

def success_respond(like_num):
    data = {}
    data["status"] = "SUCCESS"
    data["like_num"] = like_num
    return JsonResponse(data)

def error_respond(code, message):
    data = {}
    data["status"] = "ERROR"
    data["code"] = code
    data["message"] = message
    return JsonResponse(data)

# Create your views here.
def like_change(request):
    user = request.user
    if not user.is_authenticated:
        return error_respond(400, 'you were not login')

    content_type = request.GET.get("content_type")
    object_id = request.GET.get("object_id")
    print(content_type)

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        # 目标不存在
        return error_respond(401, "object does not exists.")

    is_likes = request.GET.get("is_like")

    if is_likes:
        # 要点赞
        like_record, create = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if create:
            # 没有目标,创建目标
            like_count, create = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.likes_num += 1
            like_count.save()
            return success_respond(like_count.likes_num)
        else:
            # 目标已存在,请勿重复点赞
            return error_respond(402, "object already exists.")
    else:
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有目标,删除目标
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.likes_num -= 1
                return success_respond(like_count.likes_num)
            else:
                return error_respond(403, "object doesn't exists.")

        else:
            # 没有目标,报错
            return error_respond(403, "object doesn't exists.")
