from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Code Style: Double quotation used for fields and keys
# Code Style: Single quotation used for states and URLs

# TODO: IsAuthenticated
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetchPosts(request):
    if request.method == 'GET':
        username = request.query_params.get("username")
        try:
            uploader = User.objects.get(username=username) # try-catch necessary...?
            uploader_profile = Profile.objects.get(user=uploader)
        except Profile.DoesNotExist:
            return Response({"username": username, "posts": []}, 400)

        posts = Post.objects.filter(uploader=uploader_profile)
        posts_serializer_data = []

        for post in posts:
            heart_users = []
            for heart_user in post.heart_users.all():
                heart_users.append({"nickname": heart_user.nickname})
            posts_serializer_data.append({"id": post.id, "heart_users": heart_users, "photo": post.photo, "captured_year": post.datetime.year, "captured_month": post.datetime.month, "captured_day": post.datetime.day, "captured_hour": post.datetime.hour, "captured_minute": post.datetime.minute, "caption": post.caption})
        # TODO: includes friend's photos

        ###
        # For validation purpose, pass data to serializer
        get_posts_serializer_data = {"username": username, "posts": posts_serializer_data}
        get_posts_serializer = FetchPostsSerializer(data=get_posts_serializer_data)

        if not get_posts_serializer.is_valid(raise_exception=False):
            return Response(get_posts_serializer.data, 400)
        return Response(get_posts_serializer.data, 200)

# TODO: IsAuthenticated
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

# TODO: IsAuthenticated
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postHeart(request):
    if request.method == 'POST':
        post_heart_serializer = PostHeartSerializer(data=request.data)
        if not post_heart_serializer.is_valid(raise_exception=False):
            return Response(post_heart_serializer.data, 400)
        
        post_heart_serializer.save()
        return Response(post_heart_serializer.data, 201)

@api_view(['POST'])
@permission_classes([AllowAny])
def signUp(request):
    if request.method == 'POST':
        sign_up_serializer = SignUpSerializer(data=request.data)
        
        if not sign_up_serializer.is_valid(raise_exception=False):
            return Response(sign_up_serializer.data, 400)
        
        try:
            User.objects.get(username=sign_up_serializer.validated_data['username'])
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