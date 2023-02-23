from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class Author(AbstractBaseUser):
    author_id = models.UUIDField()
    username = None
    identifier = models.CharField(max_length=40, unique=True, default=0)
    USERNAME_FIELD = "identifier"

class Post(models.Model):
    post_id = models.UUIDField()
    #user = models.ForeignKey(AbstractBaseUser)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
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