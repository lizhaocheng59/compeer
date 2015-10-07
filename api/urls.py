from rest_framework.routers import DefaultRouter

__author__ = 'Jableader'
from django.conf.urls import include, url
from rest_framework.authtoken import views as rest_views
from . import views

urlPatterns = [
    url(r'^auth/get-token', rest_views.obtain_auth_token, name='get-token'),
    url(r'^auth/register', views.register_user, name='register'),
    url(r'list/create', views.create_list, name='create_list'),
    url(r'list/(?P<list_pk>\d+)/update', views.update_item)
]

router = DefaultRouter()
router.register('list', views.ListViewSet)
router.register('auth', )