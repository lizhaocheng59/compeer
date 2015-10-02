"""compeer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from api import urls as api_urls
from compeer.settings import DEBUG

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
] + api_urls.urlPatterns

if DEBUG:
	from rest_framework.response import Response

    def say_hello(request):
        username = 'world'
        if request.user.username != '':
            username = request.user.username
        return Response('hello %s' % username)

    urlpatterns.append(url(r'^hello-world/', say_hello, name='hello_world'))
