from django.contrib.auth.base_user import BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid
import datetime

'''
Set up in the admin page
'''
class Node(models.Model):
    host = models.CharField(max_length=255)
    auth_type = models.CharField(max_length=255, default="BASIC")
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    token = models.CharField(max_length=255)


class Object(models.Model):
    type = models.TextField()
    object_id = models.CharField(max_length=255)
    actor = models.CharField(max_length=255)
    object = models.CharField(max_length=255)
    whether_comment_like = models.BooleanField(null=True)

class Follower(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    host = models.CharField(max_length=255)

    def is_friend(self, author_id):
        node = Node.objects.get(host=self.host)


class Like(models.Model):
    object_id = models.CharField(max_length=255)
    author_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    


class Profile(models.Model):
    
    type = models.CharField(max_length=100, default="Author",editable=False)
  
    id = models.CharField(max_length=100, unique=True, primary_key=True)
    url = models.URLField()
    host = models.URLField()
    displayName = models.CharField(max_length=100)
    github = models.URLField()
    profileImage = models.URLField(default='https://camo.githubusercontent.com/eb6a385e0a1f0f787d72c0b0e0275bc4516a261b96a749f1cd1aa4cb8736daba/68747470733a2f2f612e736c61636b2d656467652e636f6d2f64663130642f696d672f617661746172732f6176615f303032322d3531322e706e67', null=True)
    last_date = models.DateField(default=datetime.datetime.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Holds authentication credentials
    inbox = models.ManyToManyField(Object)
    follower_list = models.ManyToManyField(Follower, related_name='following_profiles')
    friend_list = models.ManyToManyField(Follower, related_name='friend_profiles')
    liked = models.ManyToManyField(Like)

    #DO NOT USE
    followers = models.ManyToManyField("self", related_name="users_following", symmetrical=False, blank=True)
    friends = models.ManyToManyField("self", related_name="friends_with", symmetrical=False, blank=True)


    def __str__(self):
        return self.displayName
        # return(f"{self.displayName} "
        #       f"{self.follower_list}"
        # )

class FollowRequest(models.Model):
    actor = models.CharField(max_length=255)
    object = models.CharField(max_length=255)

    # DO NOT USE
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    contentType = models.TextField(max_length=255, default='text/markdown')
    author_id = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=255, primary_key=True)
    likes = models.ManyToManyField(Like)


class Post(models.Model):

    type = models.CharField(max_length=100, default="post",editable=False)
    title = models.TextField()
    id = models.CharField(max_length=200, unique=True, primary_key=True)
    source = models.URLField()
    origin = models.URLField()
    description = models.TextField(blank=True)
    contentType = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to = "images/")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    categories = models.CharField(max_length=200, default=['web','tutorial'])
    count = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment)
    likes = models.ManyToManyField(Like)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    visibility = models.CharField(max_length=10, default="PUBLIC")
    unlisted = models.BooleanField(default=False)
    likes = models.ManyToManyField(Like)

    def __str__(self):
        return(f"{self.author} "
              f"({self.pub_date:%Y-%m-%d %H:%M}): "
              f"{self.content}"
        )

    class Meta:
        ordering = ['-pub_date']