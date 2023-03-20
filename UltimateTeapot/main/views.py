import uuid

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import Post, Profile, Comment, Like, FollowRequest

from django.shortcuts import render, redirect
from .forms import PostForm, CommentForm
from django.contrib import messages

# rest stuff
from rest_framework import viewsets
from rest_framework import permissions
from main.serializers import ProfileSerializer, PostSerializer, UserSerializer


@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        host = request.get_host()
        uniqueID = uuid.uuid4()
        authorID = "http://" + host + "/main/authors/" + str(uniqueID)

        # For the User class
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        # For the Profile class
        display_name = request.POST['displayName']
        github = request.POST["github"]
        profile_image = request.POST["profileImage"]
        
        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                #log user in and redirect to settings page
                
                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(
                    user=user_model,
                    id=authorID,
                    url=authorID,
                    host="http://"+host+"/",
                    displayName=display_name,
                    github=github,
                    profileImage=profile_image,
                )
                new_profile.followers.clear()
                new_profile.friends.clear()

                new_profile.save()
                return redirect('login')
                
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/home/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('signin')
        
    else:
        return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('signin')

def posts(request):
    posts = Post.objects.all()

    return HttpResponse(posts)

def home(request):
        form = PostForm(request.POST or None, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user.profile
                post.save()
                messages.success(request, ("You Successfully Posted!"))
                return redirect('home')

        posts = Post.objects.all().order_by("-pub_date")
        return render(request, 'home.html', {"posts":posts, "form":form})

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
    post = get_object_or_404(Post, id=post_id)
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
        post = get_object_or_404(Post, id=post_id)
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

