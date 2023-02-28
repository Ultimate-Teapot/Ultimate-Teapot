from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Author
from django.http import HttpResponse
from .models import Post
from django.shortcuts import render, redirect
from .forms import PostForm, AuthorCreationForm
from django.contrib import messages

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

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

def signup(request):
    if request.method == 'POST':
        form = AuthorCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Successful signup!")
            return redirect("main:shomepage")
    form = AuthorCreationForm()
    return render(request=request, template_name="signup.html")

# def signin(request):
#
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = auth.authenticate(username=username, password=password)
#
#         if user is not None:
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             messages.info(request, 'Credentials invalid')
#             return redirect('signin')
#
#     else:
#         return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('home')
