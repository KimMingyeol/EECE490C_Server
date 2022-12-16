from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = format_suffix_patterns ([
    path('fetch/', fetchPosts),
    path('upload/', uploadPost),
    path('signup/', signUp),
    path('login/', logIn)
])