"""new_project01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test/', views.test),

    # 主页
    url(r'^index.html$', views.index),
    url(r'^all/(?P<type_id>\d+)', views.index),

    # 登陆注册验证码
    url(r'^login.html$', views.login),
    url(r'^register.html$', views.register),
    url(r'^upload/', views.upload),
    url(r'^logout.html$', views.logout),
    url(r'^check_code/', views.check_code),

    # 个人主页
    url(r'^(?P<site>\w+).html$', views.home),

    # 筛选分类
    url(r'^(?P<site>\w+)/(?P<key>((category)|(tag)|(date)))/(?P<val>\w+-*\w*).html$',views.filter),

    # 文章详细页
    url(r'^(?P<site>\w+)/article/(?P<val>\w+).html', views.article),

    # 点赞踩
    url(r'^up_down/', views.up_down),

    # 评论
    url(r'^comments-(?P<article_nid>\w+)/', views.comments),


    # 后台管理 筛选
    url(r'^manage/all.html$', views.manage),
    url(r'^manage/(?P<article_type_id>\d+)-(?P<category_id>\d+)-(?P<tags__nid>\d+).html$', views.manage_article),

    # 后台管理 添加 文章
    url(r'^manage/add.html$', views.manage_add),
    url(r'^manage/upload_img.html$', views.upload_img),









    url(r'^app02/', include('app02.urls')),





    url(r'^', views.index),


]
