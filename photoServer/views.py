from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchPosts(request):
    if request.method == 'GET':
        username = request.query_params.get("username")
        from_which = request.query_params.get("from_which")
        try:
            uploader = User.objects.get(username=username)
            uploader_profile = Profile.objects.get(user=uploader)
        except Profile.DoesNotExist:
            return Response({"username": username, "posts": []}, 400)
        
        if from_which == "unity":
            uploader_profile.fetched_time = timezone.now()
            uploader_profile.save()

        posts = Post.objects.filter(uploader=uploader_profile)
        posts_serializer_data = []

        for post in posts:
            posts_serializer_data.append({"id": post.id, "artist": post.artist, "photo": post.photo, "captured_year": post.datetime.year, "captured_month": post.datetime.month, "captured_day": post.datetime.day, "captured_hour": post.datetime.hour, "captured_minute": post.datetime.minute, "captured_second": post.datetime.second, "caption": post.caption})
        
        get_posts_serializer_data = {"username": username, "posts": posts_serializer_data}
        get_posts_serializer = FetchPostsSerializer(data=get_posts_serializer_data)

        if not get_posts_serializer.is_valid(raise_exception=False):
            return Response(get_posts_serializer.data, 400)
        
        print(uploader_profile.fetched_time)
        print(timezone.now())
        return Response(get_posts_serializer.data, 200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadPost(request):
    # Post uploaded from an Android user
    if request.method == 'POST':
        upload_post_serializer = UploadPostSerializer(data=request.data)
        if not upload_post_serializer.is_valid(raise_exception=False):
            return Response(upload_post_serializer.data, 400)
        
        upload_post_serializer.save()
        return Response(upload_post_serializer.data, 201)

@api_view(['POST'])
@permission_classes([AllowAny])
def deletePost(request):
    if request.method == 'POST':
        post_id = request.data
        if not isinstance(post_id, int):
            return Response(-1, 400)
        
        try:
            post_to_delete = Post.objects.get(id=request.data)
        except Post.DoesNotExist:
            return Response(-1, 400)
        
        post_uploader_profile = post_to_delete.uploader
        post_uploader_profile.updated_time = timezone.now()
        post_uploader_profile.save()

        # comment out when you use an separate image storage server
        # print("Will remove", post_to_delete.photo.path, os.path.isfile(post_to_delete.photo.path))
        # if os.path.isfile(post_to_delete.photo.path):
        #     os.remove(post_to_delete.photo.path)
        
        post_to_delete.delete()
        return Response(post_id, 200)

@api_view(['POST'])
@permission_classes([AllowAny])
def signUp(request):
    if request.method == 'POST':
        sign_up_serializer = SignUpSerializer(data=request.data)
        
        if not sign_up_serializer.is_valid(raise_exception=False):
            return Response(sign_up_serializer.data, 400)
        
        try:
            sign_up_user = User.objects.get(username=sign_up_serializer.validated_data['username'])
        except User.DoesNotExist:
            sign_up_serializer.save()
            return Response(sign_up_serializer.data, 201)
        
        return Response(sign_up_serializer.data, 409)

@api_view(['POST'])
@permission_classes([AllowAny])
def logIn(request):
    if request.method == 'POST':
        log_in_serializer = LogInSerializer(data=request.data)
        if not log_in_serializer.is_valid(raise_exception=False):
            return Response(log_in_serializer.data, 400)
        
        if log_in_serializer.data['token'] == 'NOT FOUND':
            return Response(log_in_serializer.data, 401)

        return Response(log_in_serializer.data, 200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkUpdatedTime(request):
    if request.method == 'GET':
        username = request.query_params.get("username")
        try:
            uploader = User.objects.get(username=username)
            uploader_profile = Profile.objects.get(user=uploader)
        except Profile.DoesNotExist:
            return Response({"updated": False}, 400)
        
        print("checkUpdatedTime", uploader_profile.fetched_time, uploader_profile.updated_time)
        if uploader_profile.fetched_time < uploader_profile.updated_time:
            return Response({"updated": True}, 200)
        else:
            return Response({"updated": False}, 200)