from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from datetime import datetime
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login

class UserSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=30)

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField() # set to -1 when uploading
    heart_users = UserSerializer(many=True)
    photo = serializers.ImageField()
    captured_year = serializers.IntegerField()
    captured_month = serializers.IntegerField()
    captured_day = serializers.IntegerField()
    captured_hour = serializers.IntegerField()
    captured_minute = serializers.IntegerField()
    caption = serializers.CharField(max_length=50)

class FetchPostsSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    posts = PostSerializer(many=True)

class UploadPostSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=30)
    post = PostSerializer()

    def create(self, validated_data):
        if validated_data["status"] == 'ACCEPT':
            uploader = Profile.objects.get(nickname=validated_data["nickname"])
            uploaded_post = validated_data["post"]
            # Should I explicitly set heart_users?
            Post.objects.create(uploader=uploader, photo=uploaded_post.photo, datetime=datetime(year=uploaded_post.captured_year, month=uploaded_post.captured_month, day=uploaded_post.captured_day, hour=uploaded_post.captured_hour, minute=uploaded_post.captured_minute), caption=uploaded_post.caption)

        return validated_data

class PostHeartSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=30)
    target_post_id = serializers.IntegerField()

    def create(self, validated_data):
        if validated_data["status"] == 'ACCEPT':
            heart_user = Profile.objects.get(nickname=validated_data["nickname"])
            target_post = Post.objects.get(id=validated_data["id"])
            if heart_user is not None and target_post is not None:
                target_post.heart_users.add(heart_user)
        
        return validated_data

# User = get_user_model() # necessary?

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)
    nickname = serializers.CharField(max_length=30) # allow only a unique nickname

    def create(self, validated_data):
        new_user = User.objects.create(username=validated_data['username'])
        new_user.set_password(validated_data['password'])
        new_user.save()
        
        Profile.objects.create(user=new_user, nickname=validated_data['nickname'])

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