from rest_framework import serializers
from .models import *
from datetime import datetime

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField() # set to -1 when uploading
    heart_users_nickname = serializers.CharField(max_length=30, many=True)
    photo = serializers.ImageField()
    captured_year = serializers.IntegerField()
    captured_month = serializers.IntegerField()
    captured_day = serializers.IntegerField()
    captured_hour = serializers.IntegerField()
    captured_minute = serializers.IntegerField()
    caption = serializers.CharField(max_length=50)

class GetPostsSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=30)
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