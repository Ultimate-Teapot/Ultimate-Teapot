from rest_framework import viewsets
from rest_framework import permissions
from main.serializers import ProfileSerializer, PostSerializer, UserSerializer
from django.contrib.auth.models import User
from main.models import Post, Profile

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAdminUser] #Change to "IsAtuhenticated" if you want users to access the api


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]