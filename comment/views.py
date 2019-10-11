from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

from .models import Comment
from comment.forms import CommentForm

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
        data["content_type"] = ContentType.objects.get_for_model(comment).model
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
        print("data['root_pk']:{}".format(data['root_pk']))
    else:
        data["status"] = "ERROR"
        data["message"] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
