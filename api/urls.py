__author__ = 'Jableader'
from django.conf.urls import include, url
from rest_framework.authtoken import views as rest_views

urlPatterns = [
    url(r'^get-auth-token/', rest_views.obtain_auth_token)
]