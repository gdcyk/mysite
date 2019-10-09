from django.contrib import admin
from .models import Blog, BlogType
from django.core.exceptions import ObjectDoesNotExist

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'blog_type', 'content', 'get_read_num',
                    'author', 'created_time', 'last_updata_time']
    fields = ['title','created_time',  'blog_type', 'content']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(BlogAdmin, self).save_model(request, obj, form, change)

@admin.register(BlogType)
class BlogtypeAdmin(admin.ModelAdmin):
    list_display = ['type_name']

    fields = ['type_name']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(BlogtypeAdmin, self).save_model(request, obj, form, change)




