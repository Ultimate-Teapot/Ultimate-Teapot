from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class Author(AbstractBaseUser):
    id = models.UUIDField(primary_key=True)
    display_name = models.CharField(max_length=100)

    followers = models.ManyToManyField("Author", related_name='Authors_followers', blank=True)
    following = models.ManyToManyField("Author", related_name='Authors_following', blank=True)

    USERNAME_FIELD = "id"

class UserManager(BaseUserManager):
    def create_author(self, id, display_name, password):
        user = self.model(id=id)
        user.set_password(password)
        user.set_display_name(display_name)
        user.save()
        return user

class FollowRequest(models.Model):
    from_user = models.ForeignKey(Author, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Author, related_name='to_user', on_delete=models.CASCADE)

class Post(models.Model):
    post_id = models.UUIDField()
    #user = models.ForeignKey(AbstractBaseUser)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True, upload_to = "images/")
    pub_date = models.DateTimeField('date posted')
    #link = models.CharField(max_length=255, default=None)
    visibility = models.TextField()
    likes = models.IntegerField(default=0)

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
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_post_like')

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_comment_like')

class Inbox(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)