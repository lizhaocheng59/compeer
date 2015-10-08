__author__ = 'Jableader'

from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import *


class IsOwnerOrReadOnly_List(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif not request.user.is_authenticated():
            return False

        return obj.owner == request.user


class IsOwnerOrReadOnly_Item(BasePermission):
    def has_permission(self, request, view):
        if request in SAFE_METHODS:
            return True

        list_pk = request.data.get('list', None)
        if list_pk is None:
            return True

        l = List.objects.get(pk=list_pk)
        return l.owner == request.user

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.list.owner == request.user

def isOwnerOrReadOnly(klass):
    if klass == Item:
        return IsOwnerOrReadOnly_Item
    elif klass == List:
        return IsOwnerOrReadOnly_List
    else:
        raise ValueError('Unknown class type %s for IsOwnerOrReadOnly')