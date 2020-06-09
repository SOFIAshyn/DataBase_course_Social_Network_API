from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'group', 'networks', 'password')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class SocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'networks')

