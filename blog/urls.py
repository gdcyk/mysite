from django.urls import path

from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('detail/<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_type_pk>', views.blog_with_type, name='blog_with_type'),
    path('date/<int:blog_year>/<int:blog_month>/<int:blog_day>', views.blog_with_date, name='blog_with_date'),
]