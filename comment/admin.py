from django.contrib import admin

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'text', 'user',"root","parent","reply_to", 'comment_time']

