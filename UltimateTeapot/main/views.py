from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import Post, Profile
from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib import messages

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        
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
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('signup')
                
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
                post.user = request.user
                post.save()
                messages.success(request, ("You Successfully Posted!"))
                return redirect('home')

        posts = Post.objects.all().order_by("-pub_date")
        return render(request, 'home.html', {"posts":posts, "form":form})

def authors(request):
    author_list = Profile.objects.all()

    return render(request, 'authors.html', {"authors":author_list})

def profile(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)

        if request.method == "POST":
            current_user = request.user.profile

            action = request.POST['follow']
            if action == "follow":
                profile.followers.add(current_user)

            profile.save()

        return render(request, "profile.html", {"profile":profile})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

def followers(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        followers = profile.followers
        return render(request, "followers.html", {""})

