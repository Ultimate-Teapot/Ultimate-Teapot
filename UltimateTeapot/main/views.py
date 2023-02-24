from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Post
from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib import messages

def index(request):
    return HttpResponse("Hello, world. You're at the main\ index.")

def posts(request):
    posts = Post.objects.all()

    return HttpResponse(posts)

def home(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, ("You Successfully Posted!"))
                return redirect('home')

        posts = Post.objects.all().order_by("-pub_date")
        return render(request, 'home.html', {"posts":posts, "form":form})
    else:
        posts = Post.objects.all().order_by("-pub_date")
        return render(request, 'home.html', {"posts":posts})

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)