from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from datetime import datetime
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from drf_extra_fields.fields import Base64ImageField


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    artist = serializers.CharField(max_length=100, allow_blank=True)
    photo = serializers.ImageField()
    captured_year = serializers.IntegerField()
    captured_month = serializers.IntegerField()
    captured_day = serializers.IntegerField()
    captured_hour = serializers.IntegerField()
    captured_minute = serializers.IntegerField()
    captured_second = serializers.IntegerField()
    caption = serializers.CharField(allow_blank=True)

class FetchPostsSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    posts = PostSerializer(many=True)

class UploadPostSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    artist = serializers.CharField(max_length=100, allow_blank=True)
    photo = Base64ImageField()
    captured_year = serializers.IntegerField()
    captured_month = serializers.IntegerField()
    captured_day = serializers.IntegerField()
    captured_hour = serializers.IntegerField()
    captured_minute = serializers.IntegerField()
    captured_second = serializers.IntegerField()
    caption = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        uploader = User.objects.get(username=validated_data["username"])
        uploader_profile = Profile.objects.get(user=uploader)
        Post.objects.create(uploader=uploader_profile, artist=validated_data["artist"], photo=validated_data["photo"], datetime=datetime(year=validated_data["captured_year"], month=validated_data["captured_month"], day=validated_data["captured_day"], hour=validated_data["captured_hour"], minute=validated_data["captured_minute"], second=validated_data["captured_second"]), caption=validated_data["caption"])

        return validated_data

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)

    def create(self, validated_data):
        new_user = User.objects.create(username=validated_data['username'])
        new_user.set_password(validated_data['password'])
        new_user.save()

        return validated_data

class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        login_user = authenticate(username=username, password=password)

        if login_user is None:
            return {'username': username, 'password': password, 'token': 'NOT FOUND'}
        
        try:
            token = RefreshToken.for_user(login_user).access_token
            update_last_login(None, login_user)
        except User.DoesNotExist:
            return {'username': username, 'password': password, 'token': 'NOT FOUND'}

        return {'username': username, 'password': password, 'token': token}