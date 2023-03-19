from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from .models import Post, Profile
from django.shortcuts import render, redirect
from .forms import SignUpForm, UploadForm
from django.contrib import messages


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
            new_profile = Profile.objects.create(user=user_model)
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
            image = request.FILES.get('image')
            text_post = request.POST['text_post']
            if 'is_public' in request.POST and request.POST['is_public'] == 'on':
                is_public = True
            else: 
                is_public = False
            new_post = Post.objects.create(author=author_profile, image=image, text_post=text_post, is_public=is_public)
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
        # form = PostForm(request.POST or None, request.FILES)
        # if request.method == "POST":
        #     if form.is_valid():
        #         post = form.save(commit=False)
        #         post.user = request.user
        #         post.save()
        #         messages.success(request, ("You Successfully Posted!"))
        #         return redirect('home')

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
                
                if current_user in profile.users_following.all():
                    profile.friends.add(current_user)
                    current_user.friends.add(profile)
                    
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

# def followers(request, username):
#     if request.user.is_authenticated:
#         user = User.objects.get(username=username)
#         profile = Profile.objects.get(user=user)
#         followers = profile.followers
#         return render(request, "followers.html", {""})

