from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(default=0)
    followers = models.ManyToManyField("self", related_name="users_following", symmetrical=False, blank=True)
    friends =  models.ManyToManyField("self", related_name="friends_with", symmetrical=False, blank=True)
    
    def __str__(self):
        return self.user.username


# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         user_profile = Profile(user=instance)
#         user_profile.save()
#         user_profile.following.set([instance.profile.id])
#         user_profile.save()

#post_save.connect(create_profile, sender=User)

# class Author(AbstractBaseUser):
#     author_id = models.UUIDField()
#     username = None
#     identifier = models.CharField(max_length=40, unique=True, default=0)
#     USERNAME_FIELD = "identifier"

class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text_post = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to = "images/")
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    is_public = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return(f"{self.author} "
              f"({self.pub_date:%Y-%m-%d %H:%M}): "
              f"{self.text_post}"
        )

class Comment(models.Model):
    text = models.CharField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date posted')

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_post_like')

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_comment_like')

class Inbox(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)