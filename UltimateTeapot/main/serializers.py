from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Inbox
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['type','id','url','host','displayName','github','profileImage']


class PostsSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    class Meta:
        model = Post
        fields = ['title','post_id','source','origin','description','contentType','text_post','image','author','categories','count','pub_date','is_public','unlisted','likes']



# from django.contrib.auth.models import User
# from .models import Profile, Post, Comment, PostLike, CommentLike, Inbox
# from rest_framework import serializers

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'password','email']

# class ProfileSerializer(serializers.HyperlinkedModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model = Profile
#         fields = ['url','user','friends','followers']#'url', 'user', 'followers', 'friends']
    
# class PostSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['author']#'url','Post_id', 'Author', 'text', 'image', 'pub_date', 'likes']