from io import open_code
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField("Profile", blank=True)

class Post(models.Model):
    uploader = models.ForeignKey(Profile, on_delete=models.CASCADE)
    heart_users = models.ManyToManyField(Profile, blank=True, null=True, related_name="heart_users_set")
    photo = models.ImageField(upload_to='test/%Y/%m/%d')
    datetime = models.DateTimeField()
    caption = models.CharField(max_length=50, blank=True)