from django.db import models
from django.db.models import Sum, Count, Max, Min
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields import exceptions
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from read_statistics.models import ReadNum, ReadNumDetail

# Create your models here.
class BlogType(models.Model):
    type_name = models.CharField(max_length=15, default='')

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title = models.CharField(max_length=50, unique=True)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    # content = RichTextField()
    # content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField()
    # created_time = models.DateTimeField(auto_now_add=True)
    last_updata_time = models.DateTimeField(auto_now=True)
    read_num = GenericRelation(ReadNum)
    read_details = GenericRelation(ReadNumDetail)

    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            read_num = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return read_num
        except exceptions.ObjectDoesNotExist:
            return 0

    # 根据博客id统计所有日期总和的阅读量
    def get_read_num_of_date(self):
        try:
            print("本pk是:", self.pk)
            ct = ContentType.objects.get_for_model(self)

            readnumdetail_items = ReadNumDetail.objects.filter(content_type=ct, object_id=self.pk)
            readnumdetail_item_sum = 0
            for item in readnumdetail_items:
                readnumdetail_item_sum += item.read_num
            print(readnumdetail_item_sum)
            print('\n')
            return readnumdetail_item_sum
        except exceptions.ObjectDoesNotExist:
            return 0

    def __str__(self):
        return "<Blog: {}>".format(self.title)

    class Meta:
        ordering = ["-created_time"]

# class ReadNum(models.Model):
#     read_num = models.PositiveIntegerField(default=0)
#     blog = models.OneToOneField(Blog, on_delete=models.CASCADE)

