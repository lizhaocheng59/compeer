from rest_framework.routers import DefaultRouter

__author__ = 'Jableader'
from django.conf.urls import include, url
from rest_framework.authtoken import views as rest_views
from api import views

router = DefaultRouter()
router.register(r'list', views.ListViewSet)
router.register(r'item', views.ItemViewSet)

urlPatterns = [
    url(r'^auth/get-token', rest_views.obtain_auth_token, name='get-token'),
    url(r'^auth/register', views.register_user, name='register'),
    url(r'^', include(router.urls))
]