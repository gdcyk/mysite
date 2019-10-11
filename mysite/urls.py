"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from blog.views import blog_home
from comment.views import login, register, login_for_modal, logout, user_info
from likes.views import like_change

urlpatterns = [
    path('', blog_home, name='home'),
    path('admin/', admin.site.urls),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('blog/', include('blog.urls')),
    path('comment/', include("comment.urls")),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('user_info/', user_info, name='user_info'),
    path('login_for_modal/', login_for_modal, name='login_for_modal'),
    path('register/', register, name="register"),
    path('like/', like_change, name="like")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)