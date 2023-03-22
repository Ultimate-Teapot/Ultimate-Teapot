from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Post, Profile
from django.shortcuts import render, redirect
from .forms import SignUpForm, UploadForm
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404

from .serializers import ProfileSerializer

class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        
        # data = {}
        # i=1
        # for profile in profiles:
        #     data[f'author_{i}'] = {}
        #     data[f'author_{i}']['name'] = profile.user.username
        #     data[f'author_{i}']['friends'] = []
        #     for friend in profile.friends.all():
        #         data[f'author_{i}']['friends'].append(friend.user.username)
        #     i = i + 1
        
        return Response(serializer.data, status=status.HTTP_200_OK)


@login_required(login_url='login')
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
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('login')

#request.user => User => Profile
@login_required(login_url='login')
def posts(request):
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            # upload_form.save()
            current_user = User.objects.get(username=request.user)
            author_profile = Profile.objects.get(user=current_user)
            image = request.FILES.get('image')
            text_post = request.POST['text_post']
            post_type = request.POST['post_type']
            new_post = Post.objects.create(author=author_profile, image=image, text_post=text_post, post_type=post_type)
            new_post.save()
        # return render(request, 'home.html', {"upload_form":upload_form})
    #return redirect('home')
    return redirect('home')

@login_required(login_url='login')
def like(request):
    return redirect('home')

@login_required(login_url='login')
def post(request, post_id):
    #check if post_id exists
    #new_post = Post.objects.get(post_id=post_id)
    #new_post = get_object_or_404(Post, post_id=post_id)
    try:
        new_post = Post.objects.get(post_id=post_id)
    except Post.DoesNotExist:
        print("404 ERRORRRRRRRRRRRRRRRRRRR")
        return HttpResponseRedirect('/main/home/')
    
    # condition = True
    # if condition:
    #     print("SSSSSSSSSSSSSSSSSSSSSSSSS")
    #     return render(request, "post.html", {"post":new_post, "whatever": "dev"})
    # else:
    #     return HttpResponseRedirect('home')
    return render(request, "post.html", {"post":new_post, "whatever": "dev"})

@login_required(login_url='login')
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
                public_posts = Post.objects.filter(post_type=1)
                private_posts = Post.objects.filter(post_type__in=[0, 2], author=author_profile)
                private_posts_of_friends = Post.objects.none()
                my_friends = author_profile.friends.all()
                print(my_friends)
                for profile in my_friends:
                    #print(profile)
                    private_posts_of_friends |= Post.objects.filter(post_type=2, author=profile)
                    #print(private_posts_of_friends)
                unlisted_posts = Post.objects.filter(post_type=4)
                #print(current_user_friends)
                #private_posts_friends = Post.objects.filter(post_type=2, current_user_friends=current_user_friends)
                
                current_user_posts =(public_posts | private_posts | private_posts_of_friends).order_by("-pub_date")
                # print("1111111111111111111")
                # print(current_user_posts)
                # print("1111111111111111111")
        upload_form = UploadForm()
        #return render(request, 'home.html', {"posts":posts, "form":form})
        return render(request, 'home.html', {"posts":current_user_posts, "upload_form":upload_form})

def authors(request):
    author_list = Profile.objects.all()
    return render(request, 'authors.html', {"authors":author_list})

@login_required(login_url='login')
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

