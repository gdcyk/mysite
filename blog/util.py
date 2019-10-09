import datetime
from django.utils import timezone
from django.db.models import Sum

from .models import Blog
from read_statistics.models import ReadNum, ReadNumDetail

def get_seven_day_date(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7):
        date = today - timezone.timedelta(days=i)
        dates.append(date.strftime("%m/%d"))
        read_detail = ReadNumDetail.objects.filter(content_type=content_type, date=date)
        result = read_detail.aggregate(read_nums_sum=Sum('readnum'))
        read_nums.append(result)
    return dates, read_nums

def get_today_hot_blog(content_type):
    """
    根据类型统计今天阅读量
    :param content_type: 类型Blog: blog = ContentType.objects.get_for_model(BLOG)
    :return: readnum_detail: 今天安装阅读量排序的博客queryset
    """
    date = timezone.now().date()
    readnum_detail = ReadNumDetail.objects.filter(
        content_type=content_type, date=date
    ).order_by("read_num")
    return readnum_detail

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=2)
    read_details = ReadNumDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]

