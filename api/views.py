__author__ = 'Jableader'

from django.contrib.auth.models import User

from rest_framework import viewsets, status, serializers
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from . import models
from .permissions import isOwnerOrReadOnly


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
        exclude = ('score',)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = models.Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, isOwnerOrReadOnly(models.Item))

####    List    ####

class ListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.List
        exclude = ('owner',)
        extra_kwargs = {'owner': {'write_only': True}}

    def create(self, validated_data):
        model = super(ListSerializer, self).create(validated_data)
        model.owner = validated_data.get('owner')

        return model

class ListViewSet(viewsets.ModelViewSet):
    queryset = models.List.objects.all()
    serializer_class = ListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, isOwnerOrReadOnly(models.List))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)