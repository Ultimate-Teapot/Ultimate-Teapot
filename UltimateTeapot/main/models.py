from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    post_id = models.CharField(max_length=40)
    # user = models.ForeignKey(AbstractBaseUser)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True, upload_to = "images/")
    pub_date = models.DateTimeField('date posted')
    # link = models.CharField(max_length=255, default=None, null=True)
    visibility = models.TextField()
    # likes = models.IntegerField(default=0)
    

    def __str__(self):
        return(f"{self.author} "
              f"({self.pub_date:%Y-%m-%d %H:%M}): "
              f"{self.text}"
        )
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    like_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='author_post_like')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    content = models.TextField()
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_post_comment')
    created_at = models.DateTimeField(auto_now_add=True)

# class PostLike(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_post_like')

# class CommentLike(models.Model):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_comment_like')

class Inbox(models.Model):
    # author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)