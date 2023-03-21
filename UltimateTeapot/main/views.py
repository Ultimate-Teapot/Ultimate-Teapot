import json
import urllib.parse
import uuid

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.utils.http import urlencode
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import Post, Profile, Comment, Like, FollowRequest

from django.shortcuts import render, redirect
from .forms import SignUpForm, UploadForm, CommentForm
from django.contrib import messages
from django.contrib import messages

# rest stuff
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProfileSerializer, PostSerializer, UserSerializer

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

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
            authorID = "http://" + host + "/api/authors/" + str(uniqueID)
            display_name = form.cleaned_data.get('display_name')
            github = form.cleaned_data.get('github')
            profile_image = form.cleaned_data.get('profile_image')

            new_profile = Profile.objects.create(
                user=user_model,
                id=authorID,
                url=authorID,
                host="http://" + host + "/",
                displayName=display_name,
                github=github,
                profileImage=profile_image,
            )

            new_profile.followers.clear()
            new_profile.friends.clear()

            new_profile.save()

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
def upload(request):
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            # upload_form.save()
            current_user = User.objects.get(username=request.user)
            author_profile = Profile.objects.get(user=current_user)
            uniqueID = uuid.uuid4()
            post_id = author_profile.id + "/posts/" + str(uniqueID)
            image = request.FILES.get('image')
            text_post = request.POST['text_post']
            if 'is_public' in request.POST and request.POST['is_public'] == 'on':
                is_public = True
            else: 
                is_public = False
            new_post = Post.objects.create(post_id=post_id ,author=author_profile, image=image, text_post=text_post, is_public=is_public)
            new_post.save()

        #return redirect('home')
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
        
        if request.user.is_authenticated:
            if request.user.is_staff:
                current_user_posts = Post.objects.all().order_by("-pub_date")
            else:
                current_user = User.objects.get(username=request.user)
                author_profile = Profile.objects.get(user=current_user)
                public_posts = Post.objects.filter(is_public=True)
                private_posts = Post.objects.filter(is_public=False, author=author_profile)
                
                current_user_posts =(public_posts | private_posts).order_by("-pub_date")
        
         
        # else:
            #  posts = Post.objects.filter(is_public=True).order_by("-pub_date")
        upload_form = UploadForm()
        #return render(request, 'home.html', {"posts":posts, "form":form})
        return render(request, 'home.html', {"posts":current_user_posts, "upload_form":upload_form})

def inbox(request):
    
    followRequests = FollowRequest.objects.filter(receiver=request.user)
    #postMessage = Post.objects.filter(reciever = request.user)

    curr_user = request.user.profile
    following = curr_user.users_following
    post_list = []
    for user in following.all():
        print(user)
        post = Post.objects.filter(author=user)
        for p in post.all():
            post_list.append(p)
    print(post_list)

    

    
    if request.method == "POST":
        senderName = request.POST['accept']
        sender = User.objects.get(username=senderName)
        followRequest = FollowRequest.objects.get(sender=sender, receiver=request.user)


        senderProfile = followRequest.sender.profile
        receiverProfile = followRequest.receiver.profile
        receiverProfile.followers.add(senderProfile)

        if senderProfile in receiverProfile.users_following.all():
            receiverProfile.friends.add(senderProfile)
            senderProfile.friends.add(receiverProfile)

        followRequest.delete()
        return render(request, 'inbox.html', {"followRequests":followRequests})


    return render(request, 'inbox.html', {"followRequests":followRequests, "posts":post_list})

def authors(request):
    author_list = Profile.objects.all()
    return render(request, 'authors.html', {"authors":author_list})

def profile(request, id):
    if request.user.is_authenticated:
        # user = User.objects.get(username=username)
        uri = request.build_absolute_uri('?')
        profile = Profile.objects.get(id=str(uri))

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

@api_view(['GET'])
def get_authors(request):
    authors = Profile.objects.all()
    list = []
    for profile in authors:
        list.append({
            "type":"author",
            "id":profile.id,
            "host":profile.host,
            "displayName":profile.displayName,
            "url":profile.url,
            "github":profile.github,
            "profileImage":profile.profileImage,
        })

    serial = {
        "type": "authors",
        "items": list
    }

    return Response(serial)

@api_view(['GET', 'POST'])
def get_author(request, id):
    uri = request.build_absolute_uri('?')
    profile = Profile.objects.get(id=str(uri))

    serial = {
        "type":"author",
        "id":profile.id,
        "host":profile.host,
        "displayName":profile.displayName,
        "url":profile.url,
        "github":profile.github,
        "profileImage":profile.profileImage,
    }

    if request.method == 'POST': # ONLY ALLOWED ON LOCAL.
        data = request.data
        for item in data:
            if item == 'github':
                serial['github'] = data['github']
                profile.github = data['github']
                profile.save()
            elif item == 'profileImage':
                serial['profileImage'] = data['profileImage']
                profile.github = data['github']
                profile.save()
            elif item == 'displayName':
                serial['displayName'] = data['displayName']
                profile.displayName = data['displayName']
                profile.save()

        return Response(serial)

    return Response(serial)

@api_view(['GET'])
def get_followers(request):
    pass
