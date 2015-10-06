from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

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

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item

class NoListItemSerializer(ItemSerializer):
    class Meta:
        read_only_fields = ('list',)

@login_required()
@api_view(['POST', 'PUT'])
def update_item(request):
    success_status = status.HTTP_200_OK
    if request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        success_status = status.HTTP_201_CREATED
    else:
        serializer = NoListItemSerializer(data=request.data)

    errors = serializer.errors
    if request.user != serializer.instance.list.owner:
        errors['owner'] = 'You can only modify lists that you own'

    if len(errors) == 0 and serializer.is_valid():
        serializer.save()

        return Response(status=success_status)
    else:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


####    List    ####

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.List
        read_only_fields = ('owner',)

    items = serializers.StringRelatedField

    def create(self, validated_data):
        model = super(self, ListSerializer).create(validated_data)
        model.owner = validated_data.get('owner')

        return model

@login_required
@api_view(['POST', 'PUT'])
def create_list(request):
    serializer = ListSerializer(data=request.data)

    if serializer.is_valid() and not request.user.is_anonymous():
        model = serializer.save(owner=request.user)
        serializer = ListSerializer(model)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

