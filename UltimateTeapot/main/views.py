import os
import uuid

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser

from .models import Post, Profile, Comment, Like, FollowRequest, Node, Object

from django.shortcuts import render, redirect
from .forms import SignUpForm, UploadForm, CommentForm
from django.contrib import messages
from django.contrib import messages

# rest stuff
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProfileSerializer, PostsSerializer, FollowRequestSerializer, PostsPutSerializer, \
    FollowerSerializer, ProfilePostSerializer, InboxSerializer
from rest_framework.views import APIView

from django.http import Http404
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from urllib.parse import urlparse
from django.conf import settings

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def post(request, id):
    # check if post_id exist
    # for now if post doesnt exist back to home

    new_post = Post.objects.get(id=id)
    current_user = request.user.profile

    if current_user == new_post.author:
        messages.add_message(request, messages.INFO, 'You are seeing this post because you are the author.')
        return render(request, "post.html", {"post": new_post})

    elif current_user not in new_post.author.friends.all():
        # User is not authorized to view this post.
        # Redirect to a login page or display an error message.
        messages.add_message(request, messages.INFO,
                             'You cannot view this post. This is a friend posts. Only author and his/her friends can see.')
        return render(request, "not_friend.html")
    else:
        # User is authorized to view this post.
        # return render(request, 'view_post.html', {'post': post})
        return render(request, "post.html", {"post": new_post})

# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirmpassword = request.POST['confirmpassword']
        
#         if password == confirmpassword:
#             if User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email Taken')
#                 return redirect('signup')
#             elif User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username Taken')
#                 return redirect('signup')
#             else:
#                 user = User.objects.create_user(username=username, email=email, password=password)
#                 user.save()
                
#                 #log user in and redirect to settings page
                
#                 #create a Profile object for the new user
#                 user_model = User.objects.get(username=username)
#                 new_profile = Profile.objects.create(user=user_model)
#                 new_profile.save()
#                 return redirect('login')
                
#         else:
#             messages.info(request, 'Password Not Matching')
#             return redirect('signup')
#     else:
#         return render(request, 'signup.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user_model = User.objects.get(username=username)

            host = request.get_host()
            uniqueID = uuid.uuid4()
            authorID = str(uniqueID) # settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/authors/" +
            display_name = form.cleaned_data.get('display_name')
            github = form.cleaned_data.get('github')
            profile_image = form.cleaned_data.get('profile_image')

            new_profile = Profile.objects.create(
                user=user_model,
                id=authorID,
                url=settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/authors/" + authorID,
                host= settings.APP_HTTP + settings.APP_DOMAIN + "/",
                displayName=display_name,
                github=github,
                profileImage=profile_image,
            )

            new_profile.followers.clear()
            new_profile.friends.clear()

            new_profile.save()

            # new_inbox = Inbox.objects.create(
            #     author=new_profile,
            #     data={
            #     "type":"inbox",
            #     "author":authorID,
            #     "items":[]
            #     }
            # )
            # new_inbox.save()

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('signin')

    #request.user => User => Profile


@login_required(login_url='signin')
def posts(request):
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            # upload_form.save()
            current_user = User.objects.get(username=request.user)
            author_profile = Profile.objects.get(user=current_user)
            uniquePostID = uuid.uuid4()
            post_id = str(uniquePostID)
            image = request.FILES.get('image')
            content = request.POST['content']
            visibility = request.POST['visibility']
            if ('unlisted' in request.POST):
                unlisted = request.POST['unlisted']
            else:
                unlisted = False

            if (unlisted == 'on'):
                unlisted = True
            new_post = Post.objects.create(id=post_id, author=author_profile, image=image, content=content,
                                           visibility=visibility, unlisted=unlisted)
            new_post.save()

        # return redirect('home')
        # return render(request, 'home.html', {"upload_form":upload_form})
    # else:
    #     #return redirect('home')
    #     upload_form = UploadForm()

    return redirect('home')

@login_required(login_url='signin')
def like(request):
    return redirect('home')

# def posts(request):
#     posts = Post.objects.all()

#     return HttpResponse(posts)

def home(request):
        form = UploadForm(request.POST or None, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user.profile
                post.save()



                messages.success(request, ("You Successfully Posted!"))
                return redirect('home')

        # posts = Post.objects.all().order_by("-pub_date")
        #return render(request, 'home.html', {"posts":posts, "form":form})
        
        # form = PostForm(request.POST or None, request.FILES)
        # if request.method == "POST":
        #     if form.is_valid():
        #         post = form.save(commit=False)
        #         post.user = request.user
        #         post.save()
        #         messages.success(request, ("You Successfully Posted!"))
        #         return redirect('home')

        # posts = Post.objects.all().order_by("-pub_date")
        current_user_posts = None
        #author_list = Profile.objects.all()
        if request.user.is_authenticated:
            if request.user.is_staff:
                current_user_posts = Post.objects.all().order_by("-pub_date")
            else:
                current_user = User.objects.get(username=request.user)
                author_profile = Profile.objects.get(user=current_user)
                public_posts = Post.objects.filter(visibility='PUBLIC')
                # private_posts = Post.objects.filter(post_type__in=[0, 2], author=author_profile)
                # unlisted_posts = Post.objects.filter(post_type=4)
                # private_posts_of_friends = Post.objects.none()
                friend_posts = Post.objects.none()
                my_friends = author_profile.friends.all()

                for profile in my_friends:
                    friend_posts |= Post.objects.filter(visibility='FRIENDS', author=profile)

                current_user_posts = (public_posts | friend_posts).order_by("-pub_date")
                # print("HAHA: ", current_user_posts[0].visibility,current_user_posts[0].text_post )

        # res = requests.get('https://sd7-api.herokuapp.com/api/authors/d3bb924f-f37b-4d14-8d8e-f38b09703bab/posts/9095cfd8-8f6a-44aa-b75b-7d2abfb5f694/', auth=HTTPBasicAuth('node01', 'P*ssw0rd!'))
        # foreign_post = res.json()

        res2 = requests.get('https://social-t30.herokuapp.com/api/authors/15e3f8db-614c-4410-ab76-9cb737a54a95/posts/7598008a-0e75-4ca6-99fc-56ec1cba1db0/')
        foreign_post2 = res2.json()

        all_authors = []

        nodes = Node.objects.all()
        for node in nodes:
            res = requests.get(settings.APP_HTTP + node.host + "/authors", auth=HTTPBasicAuth(node.username, node.password))
            foreign_authors = res.json()
            all_authors.extend(foreign_authors['items'])


         
        # else:
            #  posts = Post.objects.filter(is_public=True).order_by("-pub_date")
        upload_form = UploadForm()
        #return render(request, 'home.html', {"posts":posts, "form":form})
        return render(request, 'home.html', {"posts":current_user_posts, "upload_form":upload_form, "authors":all_authors, "foreign_post2":foreign_post2})

def inbox(request):
    
    #followRequests = FollowRequest.objects.filter(receiver=request.user)
    #postMessage = Post.objects.filter(reciever = request.user)

    curr_user = request.user.profile
    inbox = curr_user.inbox.all()


    return render(request, 'inbox.html', {"items":inbox})

def authors(request):
    author_list = Profile.objects.all()
    return render(request, 'authors.html', {"authors":author_list})

def singlePost(request, author_id, post_id):
    if request.user.is_authenticated:

        post = Post.objects.get(id=post_id)



def profile(request, id):
    if request.user.is_authenticated:
        # user = User.objects.get(username=username)
        #uri = request.build_absolute_uri('?')
        # author_id = settings.APP_HTTP + settings.APP_DOMAIN + id

        #profile = Profile.objects.get(id=id)


        if request.method == "POST":
            current_user = request.user.profile

            action = request.POST['follow']
            if action == "follow":
                # profile.followers.add(current_user)
                #
                # if current_user in profile.users_following.all():
                #     profile.friends.add(current_user)
                #     current_user.friends.add(profile)
                if not FollowRequest.objects.filter(sender=request.user, receiver=profile.user).exists():
                    FollowRequest.objects.create(sender=request.user, receiver=profile.user)

            elif action == "unfollow":
                profile.followers.remove(current_user)
                if current_user in profile.friends.all():
                    profile.friends.remove(current_user)
                    current_user.friends.remove(profile)

            profile.save()

        return render(request, "profile.html", {"profile":profile})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

def comment_create(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    form = CommentForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.comment_author = request.user
            comment.save()
        return redirect('home')
    if request.method == 'GET':
        return render(request,"comment.html",{'form': form})
    
def like_create(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, post_id=post_id)
        like, created = Like.objects.get_or_create(post=post, like_author=request.user)
        if not created:
            like.delete()
        return redirect('home')

# def followers(request, username):
#     if request.user.is_authenticated:
#         user = User.objects.get(username=username)
#         profile = Profile.objects.get(user=user)
#         followers = profile.followers
#         return render(request, "followers.html", {""})

class NodePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='node').exists():
            return True
        return False


class AuthorList(APIView):
    # permission_classes = [NodePermission, IsAuthenticated]

    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        updated_data = {"type": "authors", "items": serializer.data}

        return Response(updated_data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.body)


class SingleAuthor(APIView):
    permission_classes = [NodePermission, IsAuthenticated]
    def get(self, request, id):

        #uri = request.build_absolute_uri('?')
        # id = request.get_full_path().split("Author/")[1]

        # o = urlparse(request)

        profile = Profile.objects.get(id=id)
        serializer = ProfileSerializer(profile)
        updated_data = serializer.data

        return Response(updated_data, status=status.HTTP_200_OK)

    def post(self, request, id, format=None):
        uri = request.build_absolute_uri('?')
        try:
            author = Profile.objects.get(id=str(uri))
        except author.DoesNotExist:
            raise Http404
        serializer = ProfilePostSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowerList(APIView):
    def get(self, request, id):
        uri = request.build_absolute_uri('?')
        uri = uri.replace("/followers", "")

        author_id = settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/authors/" + id

        author = Profile.objects.get(id=author_id)
        serializer = FollowerSerializer(author)
        updated_data = serializer.data
        return Response(updated_data, status=status.HTTP_200_OK)


class singleFollowerList(APIView):
    def get(self, request, id,fid):
        pass

    def post(self, request, id,fid):
        pass
    def put(self, request, id,fid):
        pass


class PostsList(ListCreateAPIView):
    permission_classes = [NodePermission, IsAuthenticated]

    serializer_class = PostsSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = "id"

    def perform_create(self, serializer):

        uri = self.request.build_absolute_uri('?')
       # profile_id = uri.replace("/posts/", "") # GERARD PLZ FIX MEUSDO TODOTODO TODOTODO

        #uri = self.request.build_absolute_uri('?')
        profile_id = settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/authors/" + id

        #profile_id = self.kwargs.get(self.lookup_url_kwarg)
        profile_instance = Profile.objects.get(id=profile_id)

        uniqueID = uuid.uuid4()
        post_id = uri + str(uniqueID)

        post = serializer.save(id=post_id,author=profile_instance,content=self.request.data["content"])
        return post

    # def get(self, request, id):
    #     uri = request.build_absolute_uri('?')
    #     uri = uri.replace("/posts/", "")

    #     author = Profile.objects.get(id=str(uri))
    #     posts = Post.objects.filter(author=author)
    #     serializer = PostsSerializer(posts, many=True)

    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def post(self,request,id):


class SinglePost(APIView):
    permission_classes = [NodePermission, IsAuthenticated]

    def get(self, request, id, pid):


        # uri = request.build_absolute_uri('?')
        posts = Post.objects.get(id=pid)
        serializer = PostsSerializer(posts)

        # print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id, pid, format=None):
        # uri = request.build_absolute_uri('?')
        try:
            postobj = Post.objects.get(post_id=pid)
        except postobj.DoesNotExist:
            raise Http404
        serializer = PostsSerializer(postobj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, pid, format=None):
        uri = request.build_absolute_uri('?')
        try:
            postobj = Post.objects.get(post_id=pid)
        except postobj.DoesNotExist:
            serializer = PostsPutSerializer(postobj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, pid):
        uri = request.build_absolute_uri('?')
        Post.objects.get(post_id=pid).delete()
        return Response(status=status.HTTP_200_OK)


class ImagePostsList(APIView):
    def get(self, request, id, pid):
        return Response(status=status.HTTP_200_OK)


class Commentlist(APIView):
    def get(self, request, id, pid):
        uri = request.build_absolute_uri('?')
        print(uri)
        posts = Post.objects.get(post_id=str(uri))
        serializer = PostsSerializer(posts)

        # print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,id,pid):
        return Response(status=status.HTTP_200_OK)

class FollowRequest(APIView):
    def post(self, request, id):
        followrequest = FollowRequest.objects.get(id=id)
        serializer = FollowRequestSerializer(followrequest)



class inboxLikes(APIView):
    def post(self, request, id):
        return Response(status=status.HTTP_200_OK)


class postLikes(APIView):

    def get(self, request, id,pid):
        return Response(status=status.HTTP_200_OK)


class commentLikes(APIView):

    def get(self,request,id,pid,cid):
        return Response(status=status.HTTP_200_OK)


class likedList(APIView):
    def get(self,request,id):
        return Response(status=status.HTTP_200_OK)


class InboxList(APIView):
    def get(self,request,id):
        profile = Profile.objects.get(id=id)
        serializer = InboxSerializer(profile)
        updated_data = serializer.data

        return Response(updated_data, status=status.HTTP_200_OK)

    def post(self,request,id):
        profile = Profile.objects.get(id=id)
        data = request.data
        type = data["type"]

        if type == "Follow":
            object = Object.objects.create(
                type="Follow",
                actor=data["actor"]["id"],
                object=data["object"]["id"],
            )
            profile.inbox.add(object)
            profile.save()
            return Response(status=status.HTTP_200_OK)

        elif type == "post":
            object = Object.objects.create(
                type="post",
                object_id=data["id"]
            )
            profile.inbox.add(object)
            profile.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)

    def delete(self,request,id):
        # clear the inbox
        profile = Profile.objects.get(id=id)
        profile.inbox.clear()
        profile.save()

        return Response(status=status.HTTP_200_OK)