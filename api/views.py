from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions

__author__ = 'Jableader'

from rest_framework import serializers
from django.contrib.auth.models import User

import models

####    User    ####

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        raw_password = validated_data['password']

        return User.objects.create_user(username, email, raw_password)

    def update(self, instance, validated_data):
        new_password = validated_data.get('password')
        if new_password is not None and not instance.check_password(new_password):
            instance.set_password(new_password)

@api_view(['POST', 'PUT'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

####    Item    ####

class ItemSerializer(serializers.Serializer):
    class Meta:
        read_only_fields = ('list',)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = models.Item.objects.all()
    serializer_class = models.Item
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

@login_required()
@api_view(['POST', 'PUT'])
def update_item(request, list_pk):
    list = get_object_or_404(models.List, list_pk)

    success_status = status.HTTP_200_OK
    serializer = ItemSerializer(data=request.data)

    owner_matches = (request.user == list.owner)
    if owner_matches and serializer.is_valid():
        serializer.save(list=list)

        return Response(status=success_status)
    else:
        errors = serializer.errors
        if not owner_matches:
            errors['owner'] = 'You can not add to lists you do not own'

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


####    List    ####

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.List
        read_only_fields = ('owner',)
        depth = 1

    def create(self, validated_data):
        model = super(self, ListSerializer).create(validated_data)
        model.owner = validated_data.get('owner')

        return model

class ListViewSet(viewsets.ModelViewSet):
    queryset = models.List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [Is]

@login_required
@api_view(['POST'])
def create_list(request):

    serializer = ListSerializer(data=request.data)

    if serializer.is_valid() and not request.user.is_anonymous():
        model = serializer.save(owner=request.user)
        serializer = ListSerializer(model)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_list(request, list_pk):
    list = get_object_or_404(models.List, list_pk)
    serializer = ListSerializer(instance=list)

    return Response(serializer.data, status=status.HTTP_200_OK)