"""django_blog URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from blog_site.views import *
from blog_site import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^index', views.index),
    url(r'^login', views.login),
    url(r'^register', views.register),
    url(r'^logout', views.logout),
    url(r'^findArticleList', views.findArticleList),
    url(r'^getArticleContent', views.findArticleContent),
    url(r'^createArticle', views.createArticle),
    url(r'^testUeditor', views.testUeditor),
    url(r'^saveArticles', views.saveArticles),
    url(r'^insertCategory', views.insertCategory),
    url(r'^category', views.category),
    url(r'^search', views.search),
    url(r'^createComment', views.createComment),
    url(r'^getCommentList', views.getCommentList),
    url(r'^ueditor/', include('ueditor.urls')),
    url(r'^admin/', admin.site.urls),

]
handler403 = permission_denied
handler404 = page_not_found
handler500 = page_error
