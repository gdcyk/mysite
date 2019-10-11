from datetime import datetime

from django.core.cache import cache
from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models.fields import exceptions
from django.db.models import Q
from django.db.models import Count, Sum

from .models import Blog, BlogType
from mysite.forms import LoginForm
from comment.models import Comment
from comment.forms import CommentForm
from .util import get_yesterday_hot_data
from read_statistics.models import ReadNum, ReadNumDetail

BLOG_PER_PAGE = 5


def blog_datetime(context):
    """
    统计对应日期的点击数量,用于右侧日期分类栏,注意timezone要设置为false
    :param context: 用来返回统计的结果的字典dict
    :return: None
    """
    blog_dates = Blog.objects.dates("created_time", "day", order="DESC")
    count_of_date = []
    for blog_date in blog_dates:
        blog_of_date = Blog.objects.filter(
            Q(created_time__year=blog_date.year) &
            Q(created_time__month=blog_date.month) &
            Q(created_time__day=blog_date.day)
        ).count()
        count_of_date.append(blog_of_date)
    context['blog_dates'] = zip(blog_dates, count_of_date)


def blog_paginator(request, blog_list, context):
    page_num = request.GET.get('page', default=1)
    paginator = Paginator(blog_list, BLOG_PER_PAGE)
    obj_of_blog_page = paginator.get_page(page_num)

    first = 1
    last = paginator.num_pages
    range_of_blog_page = list(range(max(int(page_num) - 2, first), min(int(page_num) + 2, last) + 1))

    if first not in range_of_blog_page:
        if range_of_blog_page[0] != first + 1:
            range_of_blog_page.insert(0, "...")
        range_of_blog_page.insert(0, first)

    if last not in range_of_blog_page:
        if range_of_blog_page[-1] != last - 1:
            range_of_blog_page.append("...")
        range_of_blog_page.append(last)

    context['blog_list'] = blog_list
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    # print(context['blog_dates'].query)
    # for item in context['blog_dates']:
    #     print(item)
    context['obj_of_blog_page'] = obj_of_blog_page
    context['range_of_blog_page'] = range_of_blog_page


def get_rank_list_of_blogs_with_pk(blogs, date_to_be_calculated):
    """
    使用博客的id作为统计的列表(自己写的,不好,没有充分利用数据库方法)
    :param blogs: 博客对象queryset
    :param date_to_be_calculated: 要统计的天数(单位:天)
    :return: 字典 dict_of_blog_read(标题:阅读量)
    """
    # 选出一段时间内阅读量最多的博客排行榜
    DATES_TO_BE_CALCULATED = date_to_be_calculated
    dict_of_blog_read = {}

    #取出每个博客在对应时间段内的阅读量
    # blogs = Blog.objects.all()
    for blog in blogs:
        # print("本pk是:", blog.pk)
        ct = ContentType.objects.get_for_model(Blog)
        today = timezone.now().date()
        date = timezone.now().date() - timezone.timedelta(days=DATES_TO_BE_CALCULATED)
        readnum_items = ReadNumDetail.objects.filter(
            content_type=ct, object_id=blog.pk, date__lte=today, date__gt=date,
        )
        result = readnum_items.aggregate(read_num_sum=Sum('read_num'))
        dict_of_blog_read.update({blog.pk: result['read_num_sum'] or 0})
    # print(dict_of_blog_read)
    # print('\n')

    # 将得到的数据按阅读量重新排
    tuple_of_blog_read = sorted(dict_of_blog_read.items(), key=lambda x: x[1], reverse=True)
    dict_of_blog_read = {}
    for item in tuple_of_blog_read:
        dict_of_blog_read.update({blogs.get(pk=item[0]).title: item[1]})
    # print(dict_of_blog_read)
    # print('\n')
    return dict_of_blog_read


def get_x_day_readnum(days):
    """
    获取所有博客days天的阅读量
    :param days: 前多少天
    :return: result 统计的queryset
    """
    today = timezone.now().date()
    date = today - timezone.timedelta(days)
    read_detail_sum = Blog.objects\
                       .filter(read_details__date__lt=today, read_details__date__gte=date)\
                       .values('pk', 'title')\
                       .annotate(read_num_sum=Sum('read_details__read_num'))\
                       .order_by('-read_num_sum')
    print(read_detail_sum)
    return read_detail_sum


def count_read_num_with_cookie(request, blog_pk, date):
    key = "blog_%s_read" % blog_pk
    if not request.COOKIES.get(key):
        ct = ContentType.objects.get_for_model(Blog)
        readnum, created_flag = ReadNum.objects.get_or_create(
            content_type=ct, object_id=blog_pk
        )
        # if ReadNum.objects.filter(content_type=ct, object_id=blog_pk).count():
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=blog_pk)
        # else:
        #     readnum = ReadNum.objects.create(content_type=ct, object_id=blog_pk)
        readnum.read_num += 1
        readnum.save()

    key2 = "blog_%s_%s_read" % (date, blog_pk)
    if not request.COOKIES.get(key2):
        ct = ContentType.objects.get_for_model(Blog)
        date = timezone.now().date()
        readnum_of_date, created_flag = ReadNumDetail.objects.get_or_create(
            content_type=ct, object_id=blog_pk, date=date
        )
        readnum_of_date.read_num += 1
        readnum_of_date.save()
    return key, key2


def blog_home(request):
    context = {}
    blogs = Blog.objects.all()

    ct = ContentType.objects.get_for_model(Blog)

    # 给七天函数增加缓存cache
    get_seven_day_hot_blog = cache.get("get_seven_day_hot_blog")
    if get_seven_day_hot_blog is None:
        get_seven_day_hot_blog = get_x_day_readnum(7)
        cache.set("get_seven_day_hot_blog", get_seven_day_hot_blog, 3600)
        print("use cache.")
    else:
        print("no cache.")

    context['blogs'] = blogs
    context['get_seven_day_hot_blog'] = get_seven_day_hot_blog
    context['get_yesterday_hot_data'] = get_yesterday_hot_data(ct)
    return render(request, 'blog_home.html', context=context)


def blog_list(request):
    blogs_list = Blog.objects.all()
    context = {}
    blog_paginator(request, blogs_list, context)
    blog_datetime(context)
    return render(request, 'blog_list.html',context=context)


def blog_detail(request, blog_pk):
    context = {}
    current_blog = get_object_or_404(Blog, pk=blog_pk)
    date = timezone.now().date()

    key, key2 = count_read_num_with_cookie(request, blog_pk, date)

    previous_blog = Blog.objects.filter(created_time__lt=current_blog.created_time).last()
    next_blog = Blog.objects.filter(created_time__gt=current_blog.created_time).first()
    context['blog'] = current_blog
    context['previous_blog'] = previous_blog
    context['next_blog'] = next_blog
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['login_forms'] = LoginForm()
    blog_datetime(context)
    respond = render(request, 'blog_detail.html', context=context)
    respond.set_cookie(key, "True")
    respond.set_cookie(key2, "True")
    return respond


def blog_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_list = Blog.objects.filter(blog_type=blog_type)

    context = {}
    blog_paginator(request, blogs_list, context)
    blog_datetime(context)
    context['blog_type'] = blog_type

    return render(request, 'blog_with_type.html', context=context)
    # return render_to_response('blog_with_type.html', context=context)


def blog_with_date(request, blog_year=None, blog_month=None, blog_day=None):
    blogs_list = Blog.objects.filter(created_time__year=blog_year,
                                     created_time__month=blog_month,
                                     created_time__day=blog_day)
    context = {}
    blog_paginator(request, blogs_list, context)
    blog_datetime(context)
    return render(request, 'blog_with_date.html', context=context)
    # return render_to_response('blog_with_date.html', context=context)