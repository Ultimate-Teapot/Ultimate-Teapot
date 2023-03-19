from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    id = models.CharField(max_length=100, unique=True, primary_key=True)
    host = models.URLField()
    displayName = models.CharField(max_length=100)
    url = models.URLField()
    github = models.URLField()
    profileImage = models.URLField()
    last_date = models.DateField()

    followers = models.ManyToManyField("self", related_name="users_following", symmetrical=False, blank=True)
    friends = models.ManyToManyField("self", related_name="friends_with", symmetrical=False, blank=True)

    def __str__(self):
        return self.displayName

class FollowRequest(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)

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
    post_id = models.CharField(max_length=40)
    # user = models.ForeignKey(AbstractBaseUser)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True, upload_to = "images/")
    pub_date = models.DateTimeField('date posted')
    # link = models.CharField(max_length=255, default=None, null=True)
    visibility = models.TextField()
    likes = models.IntegerField(default=0)


    #sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    #receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)

    def __str__(self):
        return(f"{self.author} "
              f"({self.pub_date:%Y-%m-%d %H:%M}): "
              f"{self.text}"
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