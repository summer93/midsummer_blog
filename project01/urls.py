"""project01 URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index.html$', views.index),
    url(r'^all/(?P<type_id>\d+)', views.index),
    url(r'^login.html$', views.login),
    url(r'^register.html$', views.register),
    url(r'^upload/', views.upload),
    url(r'^logout.html$', views.logout),
    url(r'^check_code/', views.check_code),


    url(r'^(?P<site>\w+).html$', views.userblog),
    url(r'^(?P<site>\w+).html/tag/(?P<tag>\w+)', views.userblog),
    url(r'^(?P<site>\w+).html/category/(?P<category>\w+)', views.userblog),

    url(r'^', views.index),
]












