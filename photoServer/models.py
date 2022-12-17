from io import open_code
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Post(models.Model):
    uploader = models.ForeignKey(Profile, on_delete=models.CASCADE)
    artist = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='test/%Y/%m/%d')
    datetime = models.DateTimeField()
    caption = models.TextField(blank=True)