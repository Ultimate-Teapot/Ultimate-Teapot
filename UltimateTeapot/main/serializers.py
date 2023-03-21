from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Inbox
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'password','email']

class ProfileSerializer(serializers.Serializer):
    #user = UserSerializer()

    type = "author"
    id = serializers.CharField(max_length=100)
    host = serializers.URLField()
    displayName = serializers.CharField(max_length=100)
    url = serializers.URLField()
    github = serializers.URLField()
    profileImage = serializers.URLField()

    # class Meta:
    #     model = Profile
    #     fields = ['id','url','host','displayName', 'github', 'profileImage']
    
class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['author']#'url','Post_id', 'Author', 'text', 'image', 'pub_date', 'likes']

