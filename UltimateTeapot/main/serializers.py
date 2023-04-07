from django.contrib.auth.models import User
from requests.auth import HTTPBasicAuth

from .models import Profile, Post, Comment, FollowRequest, Object, Node, Like
from rest_framework import serializers

from rest_framework.serializers import CharField, DateTimeField, IntegerField
from .requestsHelper import get_request, post_request

from rest_framework.serializers import CharField, DateTimeField
from django.conf import settings
from urllib.parse import urlparse
import requests

import uuid
import base64




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['type','id','url','host','displayName','github','profileImage']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = "author"
        representation['id'] = settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/authors/" + instance.id
        return representation

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = "followers"
        items = []
        for follower in instance.follower_list.all():
            follower_id = follower.id
            follower_host = follower.host
            follower_node = Node.objects.get(host=follower_host)

            follower_data = get_request(follower_id + '/', follower_node)
            items.append(follower_data)

        representation['items'] = items

        return representation



class PostsSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required = False,read_only=True)
    title = CharField(required=True)
    type = CharField(read_only=True)
    categories = serializers.SerializerMethodField('get_categories')
    comments = serializers.SerializerMethodField('get_comments')
    id = CharField(required = False, read_only = True)
    count = IntegerField(required=False,read_only=True)
    source = serializers.SerializerMethodField("get_source",required=False)
    origin = serializers.SerializerMethodField("get_origin",required=False)


    def get_source(self,instance):
        return instance.id
        
    def get_origin(self,instance):
        return instance.id

    def get_categories(self, instance):
        return ['web','tutorial','hack']
    
    def get_comments(self, instance):
        return "TODO"

    published = DateTimeField(read_only=True,required=False,source="pub_date")

    class Meta:
        model = Post
        fields = ['type','title','id','source','origin','description','contentType','content','author','categories','count','comments','published','visibility','unlisted'] # add back is_public


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = "post"
        representation['id'] = settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/authors/" + instance.author.id + "/posts/" + instance.id
        return representation

    


class PostSerializer(serializers.ModelSerializer):
    type = CharField(read_only=True)
    title = CharField(required=True)
    id = CharField(required=False,read_only=True)
    # source = URLField(allow_blank=True)
    # origin = URLField(allow_blank=True)
    description=CharField(allow_blank=True)
    contentType=CharField(allow_blank=True)
    content = CharField(allow_blank=True)
    author = ProfileSerializer(required = False,read_only=True)
    categories = serializers.SerializerMethodField('get_categories')
    count = IntegerField(required=False,read_only=True)
    comments = serializers.SerializerMethodField('get_comments')
    #unlisted = BooleanField(allow_blank=True)
    #likes = IntegerField(required=False,read_only=True)
    published = DateTimeField(source="pub_date",read_only=True)
    source = serializers.SerializerMethodField("get_source",required=False)
    origin = serializers.SerializerMethodField("get_origin",required=False)
    
   


    def get_source(self,instance):
        return instance.id
        
    def get_origin(self,instance):
        return instance.id

    def get_categories(self, instance):
        return ['web','tutorial','hack']
    
    def get_comments(self, instance):
        return "TODO"


    # ADD PERMISSIONS FOR PUT #   
    def create(self,validated_data):
        return Post.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
     instance.title = validated_data.get('title', instance.title)
     instance.description = validated_data.get('description', instance.description)      
     instance.content = validated_data.get('content', instance.content)    
     instance.contentType = validated_data.get('contentType', instance.contentType) 
     instance.unlisted = validated_data.get('unlisted',instance.unlisted)
     instance.save()
     return instance
    

    def get_fields(self, *args, **kwargs):
            fields = super().get_fields(*args, **kwargs)
            request = self.context.get('request', None)
            if request and getattr(request, 'method', None) == "POST":
                fields['id'].read_only = True
            return fields


    class Meta:
        model = Post
        fields = ['type','title','id','source','origin','description','contentType','content','author','categories','count','comments','published','visibility','unlisted'] # add back is_public
        
        #extra_kwargs = {'title': {'write_only': True},'description': {'write_only': True},'content': {'write_only': True},'published': {'write_only': True},'unlisted': {'write_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/authors/" + instance.author.id + "/posts/" + instance.id
        return representation

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = "comment"
        author_id = instance.author_id
        host = author_id.split("authors")[0]
        if "/api" in host:
            author_node = Node.objects.get(host=host)
        else:
            host = host + "api/"
            author_node = Node.objects.get(host=host)

        real_id = host + "authors/" + author_id.split('authors/')[1] + "/"

        author_json = get_request(real_id, author_node)
        representation['author'] = author_json
        representation['comment'] = instance.comment
        representation['published'] = instance.created_at
        representation['id'] = instance.id

        return representation


#TODO: make sure comments lists work, add pagination
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["type"] = "comments"
        post_id = settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/authors/" + instance.author.id + "/posts/" + instance.id
        representation["post"] = post_id
        representation["id"] = post_id + "/comments"
        comments = []

        for comment in instance.comments.all():
            comment = CommentSerializer(comment).data
            comments.append(comment)

        representation["comments"] = comments

        return representation

################################################################################################

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']

################################################################################################################################

class PostsPutSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    class Meta:
        model = Post
        fields = ['type','title','id','source','origin','description','contentType','content','author','categories','count','pub_date','unlisted','likes'] # add back is_public

class FollowRequestSerializer(serializers.ModelSerializer):
    # actor = ProfileSerializer()
    # object = ProfileSerializer()
    class Meta:
        model = Object
        fields = ['type']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        actor_id = instance.actor
        #actor_url = urlparse(actor_id)
        host = actor_id.split('authors')[0]

        node = Node.objects.get(host=host)
        actor_json = get_request(actor_id + '/', node)

        object_id = instance.object
        object_json = ProfileSerializer(Profile.objects.get(url=object_id)).data

        representation['type'] = "Follow"
        representation['summary'] = actor_json["displayName"] + " wants to follow " + object_json["displayName"]

        representation['actor'] = actor_json
        representation['object'] =object_json

        return representation

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['@context'] = "https://www.w3.org/ns/activitystreams"

        author_id = instance.author_id
        host = author_id.split("author")[0]
        node = Node.objects.get(host=host)
        author_json = get_request(author_id + '/', node)

        representation['summary'] = author_json['displayName'] = " likes your post"
        representation['type'] = "Like"
        representation['author'] = author_json
        representation['object'] = instance.object_id

        return representation

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['type']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = "likes"
        items = []

        for like in instance.likes.all():
            like_data = LikeSerializer(like).data
            items.append(like_data)

        representation['items'] = items

        return representation

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = "likes"
        items = []

        for like in instance.likes.all():
            like_data = LikeSerializer(like).data
            items.append(like_data)

        representation['items'] = items

        return representation

class AuthorLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = "likes"
        items = []

        for like in instance.liked.all():
            like_data = LikeSerializer(like).data
            items.append(like_data)

        representation['items'] = items

        return representation

class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['type']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = "inbox"
        representation['author'] = settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/authors/" + instance.id

        items = []
        for item in instance.inbox.all():
            if item.type == "Follow":
                follow = FollowRequestSerializer(item).data
                items.append(follow)
            elif item.type == "post":
                id = item.object_id
                # actor_url = urlparse(actor_id)
                host = id.split('authors')[0]


                node = Node.objects.get(host=host)
                post_json = get_request(id + '/', node)

                items.append(post_json)
            elif item.type == "comment":
                id = item.object_id
                comment = Comment.objects.get(id=id)
                comment_json = CommentSerializer(comment).data
                items.append(comment_json)

            elif item.type == "like":
                object_id = item.object_id
                like = Like.objects.get(object_id=object_id)
                like_json = LikeSerializer(like).data
                items.append(like_json)



        representation['items'] = items

        return representation


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