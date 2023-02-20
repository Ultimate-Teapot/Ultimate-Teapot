from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class Author(AbstractBaseUser):
    author_id = models.UUIDField()

class Post(models.Model):
    post_id = models.UUIDField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    image = models.ImageField()
    pub_date = models.DateTimeField('date posted')
    link = models.CharField(max_length=255)
    visibility = models.TextField()
    likes = models.IntegerField()

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