from django.contrib.auth.models import User
from requests.auth import HTTPBasicAuth

from .models import Profile, Post, Comment, FollowRequest, Object, Node
from rest_framework import serializers
from rest_framework.serializers import CharField, DateTimeField
from django.conf import settings
from urllib.parse import urlparse
import requests

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['type','id','url','host','displayName','github','profileImage']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/authors/" + instance.id
        return representation

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['followers']

class ProfilePostSerializer(serializers.ModelSerializer):
    # TODO: not needed?
    class Meta:
        model = Profile
        fields = ['type', 'id', 'url','host','displayName','github','profileImage']

    def update(self,instance,validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.id = validated_data.get('id', instance.id)
        instance.url = validated_data.get('url',instance.url)
        instance.host = validated_data.get('host',instance.host)
        instance.displayName = validated_data.get('displayName',instance.displayName)
        instance.github = validated_data.get('github',instance.github)
        instance.profileImage= validated_data.get('profileImage',instance.profileImage)
        instance.save()
        return instance

class PostsSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required = False,read_only=True)
    title = CharField(required=True)
    type = CharField(read_only=True)
    categories = serializers.SerializerMethodField('get_categories')
    comments = serializers.SerializerMethodField('get_comments')
    
    def get_categories(self, instance):
        return ['web','tutorial','hack']
    
    def get_comments(self, instance):
        return "TODO"

    published = DateTimeField(source="pub_date")

    class Meta:
        model = Post
        fields = ['type','title','id','source','origin','description','contentType','content','author','categories','count','comments','published','unlisted','likes'] # add back is_public

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/authors/" + instance.author.id + "/posts/" + instance.id
        return representation

    # def create(self,validated_data):
    #     return Post.objects.create(**validated_data)

    # def update(self, instance, validated_data):

    #     if 'author' in validated_data:
    #         nested_serializer = self.fields['author']
    #         nested_instance = instance.author
    #         nested_data = validated_data.pop('author')
    #         nested_serializer.update(nested_instance, nested_data)


    #     instance.title = validated_data.get('title',instance.title)
    #     instance.source = validated_data.get('source',instance.source)
    #     instance.origin = validated_data.get('origin',instance.origin)
    #     instance.description = validated_data.get('description',instance.description)
    #     instance.contentType = validated_data.get('contentType',instance.contentType)
    #     instance.text_post = validated_data.get('text_post',instance.text_post)
    #     instance.image = validated_data.get('image',instance.image)
    #     instance.author = validated_data.get('author',instance.author)
    #     instance.categories = validated_data.get('categories',instance.categories)
    #     instance.count = validated_data.get('count',instance.count)
    #     instance.pub_date = validated_data.get('pub_date',instance.pub_date)
    #     instance.unlisted = validated_data.get('unlisted',instance.unlisted)
    #     instance.likes = validated_data.get('likes',instance.likes)

    #     return super(PostsSerializer,self).update(instance,validated_data)

class PostsPutSerializer(serializers.ModelSerializer):
    author = ProfilePostSerializer()
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
        root = actor_id.split('/authors')[0]
        host = root.split('//')[1]

        node = Node.objects.get(host=host)
        actor_object = requests.get(actor_id, auth=HTTPBasicAuth(node.username, node.password))
        actor_json = actor_object.json()

        object_id = instance.object
        object_json = ProfileSerializer(Profile.objects.get(url=object_id)).data

        representation['type'] = "Follow"
        representation['summary'] = actor_json["displayName"] + " wants to follow " + object_json["displayName"]

        representation['actor'] = actor_json
        representation['object'] =object_json

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
                root = id.split('/authors')[0]
                host = root.split('//')[1]

                node = Node.objects.get(host=host)
                post = requests.get(id, auth=HTTPBasicAuth(node.username, node.password))
                post_json = post.json()

                items.append(post_json)



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