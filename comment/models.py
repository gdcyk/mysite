from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)

    root = models.ForeignKey("self", on_delete=models.CASCADE, related_name="root_comment", null=True, default=None)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="parent_comment", null=True, default=None)
    reply_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies", null=True, default=None)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["comment_time"]
