from django.contrib.auth.base_user import BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid
import datetime

class Object(models.Model):
    # post, comment, like or FollowRequest
    type = models.TextField()
    # If the object is post, comment or like:
    object_id = models.CharField(max_length=255)

    # If the object is a follow request:
    actor = models.CharField(max_length=255)
    object = models.CharField(max_length=255)

class Follower(models.Model):
    # id as url
    id = models.CharField(max_length=255, primary_key=True)
    # host as url
    host = models.CharField(max_length=255)

class Profile(models.Model):
    # TO BE SENT AS JSON #
    type = models.CharField(max_length=100, default="Author",editable=False)
    # UUID only
    id = models.CharField(max_length=100, unique=True, primary_key=True)
    url = models.URLField()
    host = models.URLField()
    displayName = models.CharField(max_length=100)
    github = models.URLField()
    profileImage = models.URLField()
    
    last_date = models.DateField(default=datetime.datetime.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Holds authentication credentials

    inbox = models.ManyToManyField(Object)

    follower_list = models.ManyToManyField(Follower, related_name='following_profiles')
    friend_list = models.ManyToManyField(Follower, related_name='friend_profiles')
    # Test these two later with postgres
    # List of authorIDs that are followers
    #follower_list = ArrayField(
    #    models.CharField(max_length=255)
    #)

    # List of authorIDs that are friends
    #friend_list = ArrayField(
    #    models.CharField(max_length=255)
    #)

    #DO NOT USE
    followers = models.ManyToManyField("self", related_name="users_following", symmetrical=False, blank=True)
    friends = models.ManyToManyField("self", related_name="friends_with", symmetrical=False, blank=True)


    def __str__(self):
        #return self.displayName
        return(f"{self.displayName} "
              f"{self.follower_list}"
        )

class FollowRequest(models.Model):
    # id of author sending the request
    actor = models.CharField(max_length=255)
    # id of author recieving the request
    object = models.CharField(max_length=255)

    # DO NOT USE
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

    # Type of post #
    type = models.CharField(max_length=100, default="post",editable=False)
    #Title of Post
    title = models.TextField()
    #Post ID (UUID)
    id = models.CharField(max_length=200, unique=True, primary_key=True)
    #Source
    source = models.URLField()
    #origin
    origin = models.URLField()
    #description
    description = models.TextField(blank=True)
    #Conent-type
    contentType = models.CharField(max_length=100)
    #Content
    content = models.TextField()
    #markdown_content = models.TextField()

    image = models.ImageField(null=True, blank=True, upload_to = "images/")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # URL, not uuid
    #author_id = models.CharField(max_length=255)

    #categories
    categories = models.CharField(max_length=200, default=['web','tutorial'])
    #count - the count of comments on the post
    count = models.IntegerField(default=0)
    

    #TO_DO ADD COMMENTS AND COMMENT SRC



    # Url to comments
    comments = models.CharField(max_length=255)



    #Published
    #pub_date = models.DateTimeField(auto_now=False,auto_now_add=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    #Visibility
    visibility = models.CharField(max_length=10, default="PUBLIC")
    #Unlisted
    unlisted = models.BooleanField(default=False)


    # post_type = models.IntegerField(default=0)

    likes = models.IntegerField(default=0)

    def __str__(self):
        return(f"{self.author} "
              f"({self.pub_date:%Y-%m-%d %H:%M}): "
              f"{self.content}"
        )
    
class Like(models.Model):
    # id of the object being liked as url
    object_id = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    # Please DO NOT USE
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    like_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='author_post_like')


class Comment(models.Model):
    # Post id stored as url
    post_id = models.CharField(max_length=255)
    content = models.TextField()
    contentType = models.TextField(max_length=255, default='text/markdown')
    # author object
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # uuid of comment
    id = models.CharField(max_length=255, primary_key=True)

    # DO NOT USE
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_post_comment')
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')

# class PostLike(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_post_like')

# class CommentLike(models.Model):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_comment_like')



# class Inbox(models.Model):
#     # author = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     # sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_messages')
#     # recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages')
#     # content = models.TextField()
#     # timestamp = models.DateTimeField(auto_now_add=True)
#     author = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
#     items = models.ManyToManyField(Object)
#
#     # DO NOT USE
#     data = models.JSONField(default=dict, blank=True, null=True)

'''
Set up in the admin page
'''
class Node(models.Model):
    # service we are connecting to
    host = models.CharField(max_length=255)
    # Our username for the service
    username = models.CharField(max_length=255)
    # Our password for the service
    password = models.CharField(max_length=255)