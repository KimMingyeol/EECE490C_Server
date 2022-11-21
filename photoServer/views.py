from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Create your views here.
# Code Style: Double quotation used for fields and keys
# Code Style: Single quotation used for states

# TODO: IsAuthenticated
@api_view(['GET'])
@permission_classes([AllowAny])
def fetchPosts(request):
    if request.method == 'GET':
        nickname = request.query_params.get("nickname")
        uploader = Profile.objects.get(nickname=nickname)
        if uploader is None:
            return Response({"nickname": nickname, "posts": []}, 400)

        posts = Post.objects.filter(uploader=uploader)
        posts_serializer_data = []

        for post in posts:
            heart_users_nickname = []
            for heart_user in post.heart_users.all():
                heart_users_nickname.append(heart_user.nickname)
            posts_serializer_data.append({"id": post.id, "heart_users_nickname": heart_users_nickname, "photo": post.photo, "captured_year": post.datetime.year, "captured_month": post.datetime.month, "captured_day": post.datetime.day, "captured_hour": post.datetime.hour, "captured_minute": post.datetime.minute, "caption": post.caption})
        # TODO: includes friend's photos

        ###
        # For validation purpose, pass data to serializer
        get_posts_serializer_data = {"nickname": nickname, "posts": posts_serializer_data}
        get_posts_serializer = GetPostsSerializer(data=get_posts_serializer_data)

        if not get_posts_serializer.is_valid(raise_exception=False):
            return Response(get_posts_serializer.data, 400)
        return Response(get_posts_serializer.data, 200)

# TODO: IsAuthenticated
@api_view(['POST'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def postHeart(request):
    if request.method == 'POST':
        post_heart_serializer = PostHeartSerializer(data=request.data)
        if not post_heart_serializer.is_valid(raise_exception=False):
            return Response(post_heart_serializer.data, 400)
        
        post_heart_serializer.save()
        return Response(post_heart_serializer.data, 201)