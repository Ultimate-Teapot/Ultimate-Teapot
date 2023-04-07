import base64
import datetime
import json
import os
import urllib.parse
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
from .requestsHelper import get_request, post_request
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAdminUser

from .models import Post, Profile, Comment, Like, FollowRequest, Node, Object, Follower
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .forms import SignUpForm, UploadForm, CommentForm, ProfileForm
from django.contrib import messages
from django.contrib import messages

# rest stuff
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProfileSerializer, PostsSerializer, FollowRequestSerializer, PostSerializer, \
    FollowerSerializer, InboxSerializer, PostImageSerializer, CommentSerializer, CommentListSerializer, \
    PostLikeSerializer, CommentLikeSerializer, AuthorLikeSerializer
from rest_framework.views import APIView

from django.http import Http404
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from urllib.parse import urlparse
from django.conf import settings
from django.core.files.base import ContentFile
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.db.models.query import QuerySet


def teapot(request):
    return render(request, 'teapot.html', status=418)

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

    return render(request, "post.html", {"post": new_post})

def foreign_post(request, id):
    # Pass in the full URL of a post, make a get request and display it on a page
    # Make comments
    comment_form = CommentForm(request.POST or None)


    host = id.split("authors/")[0]
    if host == settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/":
        # Local
        post_uuid = id.split("/posts/")[1]
        try:
            post = Post.objects.get(id=post_uuid)
        except Post.DoesNotExist:
            return Http404

        post_json = PostSerializer(post).data
        post_comments_list = CommentListSerializer(post).data['comments']

    else:
        # Remote
        node = Node.objects.get(host=host)
        post_json = get_request(id + '/', node)
        try:
            post_comments_json = get_request(id + '/comments/', node)
        except json.JSONDecodeError:
            try:
                post_comments = get_request(id + '/comments', node)
                post_comments_list = post_comments['comments']
            except json.JSONDecodeError:
                post_comments_json = None

    return render(request, "foreign_post.html", {"post":post_json, "comments":post_comments_list, "comment_form":comment_form})


def delete_post(request, id):
    uuid = id.split("posts/")[1]
    post = Post.objects.get(id = uuid)
    post.delete()
    return redirect('home')

def edit_post(request, id):
    uuid = id.split("posts/")[1]
    post = Post.objects.get(id = uuid)
    form = UploadForm(request.POST or None, instance=post)
    if request.method == "POST":
        if form.is_valid():
            form.contentType = post.contentType
            form.save()
            messages.success(request, ("You Successfully Edited!"))
            return redirect('home')
    #upload_form = UploadForm()
 
    return render(request, "edit_post.html", {"post":post, "upload_form":form})


# def edit_profile(request,id):
#     if request.user.is_authenticated:
#         uuid = id.split("/authors/")[1]
#         profile = Profile.objects.get(id=uuid)

#         form = SignUpForm(request.POST or None, instance=profile)
#         if request.method == 'POST':

#             if form.is_valid():
#                 form.save()

#         return render(request, "edit_profile.html", {"profile": profile, "form": form})
#     else:
#         messages.success(request, ("You must be logged in to view this page"))
#         return redirect('home')

#     return render(request, "edit_profile.html")#, {"profile":oldprofile}) #"upload_form":form, 

@login_required
def edit_profile(request, id):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, "edit_message.html")
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

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


            # if form.fields['profile_image']=="":
            #     form.fields['profile_image'].initial = "https://i.imgur.com/lu0eCzU.jpeg"

            profileImage = form.cleaned_data.get('profile_image')
            
            if profileImage == None:
                profileImage = "https://camo.githubusercontent.com/eb6a385e0a1f0f787d72c0b0e0275bc4516a261b96a749f1cd1aa4cb8736daba/68747470733a2f2f612e736c61636b2d656467652e636f6d2f64663130642f696d672f617661746172732f6176615f303032322d3531322e706e67"


            new_profile = Profile.objects.create(
                user=user_model,
                id=authorID,
                url=settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/authors/" + authorID,
                host= settings.APP_HTTP + settings.APP_DOMAIN + "/",
                displayName=display_name,
                github=github,
                profileImage=profileImage,
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
    print("in posts")
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            # upload_form.save()
            current_user = User.objects.get(username=request.user)
            author_profile = Profile.objects.get(user=current_user)
            uniquePostID = uuid.uuid4()
            post_id = str(uniquePostID)
            #image = request.FILES.get('image')

            contentType = request.POST['contentType']
            image = request.FILES.get('image')
            # image = request.POST('image')
            content = request.POST['content']

            # See what to set content type to #
            if image:
                try:
                    if ".png" in image.name:
                        contentType = "image/png;base64"
                    if (".jpeg" in image.name) or (".jpg" in image.name):
                        contentType = "image/jpeg;base64"
                except:
                    contentType = "application/base64"
             

            if (contentType == "image/png;base64") or (contentType == "image/jpeg;base64") or (contentType == "application/base64"):
                image = request.FILES.get('image')

                # how to decode base 64 taken from
                #  https://stackoverflow.com/questions/6375942/how-do-you-base-64-encode-a-png-image-for-use-in-a-data-uri-in-a-css-file
                b_64 = base64.b64encode(image.file.read()).decode('ascii')
                content = "data:"+ contentType + "," + b_64

               
            else:
                content = request.POST['content']


            visibility = request.POST['visibility']

            if visibility == "FRIENDS":
                current_user = request.user.profile
                actor = ProfileSerializer(current_user).data
                print("INSIDE FRIEND POSTS")

                for friend in current_user.friend_list.all():
                    id = friend.id
                    target_host = id.split("author")[0]
                    target_node = Node.objects.get(host=target_host)

                    object = requests.get(id + '/', auth=HTTPBasicAuth(target_node.username, target_node.password))
                    object_json = object.json()
                    data_to_send = {
                        "type": "post",
                        "summary": actor['displayName'] + " has posted a new friend post. ",
                        # display the uRL later maybe?
                        "author": actor,
                        "object": object_json,
                        "id": actor['id'] + "/posts/" + post_id,
                    }

                    requests.post(id + "/inbox/", json=data_to_send,
                                  auth=HTTPBasicAuth(target_node.username, target_node.password))

            title = request.POST['title']
            if ('unlisted' in request.POST):
                unlisted = request.POST['unlisted']
            else:
                unlisted = False
            if (unlisted == 'on'):
                unlisted = True

            # pub_date = datetime.datetime.now().isoformat()

            new_post = Post.objects.create(title=title,id=post_id, author=author_profile, content=content,
                                           visibility=visibility, unlisted=unlisted,contentType=contentType)
            new_post.save()
           

    return redirect('home')

@login_required(login_url='signin')
def make_comment(request, id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            uniqueCommentID = uuid.uuid4()
            comment_id = str(uniqueCommentID)
            comment = request.POST['comment']

            profile = request.user.profile
            author_data = ProfileSerializer(profile).data

            pub_date = datetime.datetime.now().isoformat()
            full_id = id + "/comments/" + comment_id

            obj_json = {
                "type":"comment",
                "author":author_data,
                "comment":comment,
                "contentType":"text/markdown",
                "published":pub_date,
                "id":full_id
            }

            author_id = id.split("/posts/")[0]
            host = author_id.split("authors/")[0]

            node = Node.objects.get(host=host)
            post_request(author_id + "/inbox/", node, obj_json)

    return redirect('foreign_post', id)

@login_required(login_url='signin')
def like_post(request, id):
    if request.method == 'POST':
        profile = request.user.profile
        author_data = ProfileSerializer(profile).data

        obj_json = {
            "@context":"https://wwww.w3.org/ns/activitystreams",
            "summary":profile.displayName + " likes your post",
            "type":"Like",
            "author":author_data,
            "object":id,
        }

        print(obj_json)

        author_id = id.split("/posts/")[0]
        host = author_id.split("authors/")[0]

        node = Node.objects.get(host=host)
        post_request(author_id + "/inbox/", node, obj_json)


    return redirect('foreign_post', id)

@login_required(login_url='signin')
def like_comment(request, id):
    if request.method == 'POST':
        profile = request.user.profile
        author_data = ProfileSerializer(profile).data
        # comment_instance = Comment.objects.get(id=id)
        # comment_author_id = comment_instance.author_id


        obj_json = {
            "@context":"https://wwww.w3.org/ns/activitystreams",
            "summary":profile.displayName + " likes the comments",
            "type":"Like",
            "author":author_data,
            "object":id,
        }

        print(obj_json)


        author_id = id.split("/posts/")[0]
        host = author_id.split("authors/")[0]
        

        node = Node.objects.get(host=host)
        post_request(author_id + "/inbox/", node, obj_json)

    post_id = id.split("/comments/")[0]

    return redirect('foreign_post', post_id)

@login_required(login_url='signin')
def like(request):
    return redirect('home')


def make_post(request):
    upload_form = UploadForm()
    #return render(request, 'home.html', {"posts":posts, "form":form})
    return render(request, 'make_post.html', {"upload_form":upload_form})


def home(request):
        
        current_user_posts = None

        viewable_posts = []
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

                all_authors_posts = []
                nodes = Node.objects.all()
                for node in nodes:

                    if node.host == settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/":
                        for local_post in Post.objects.filter(visibility="PUBLIC"):
                            print(PostSerializer(local_post).data)
                            all_authors_posts.append(PostSerializer(local_post).data)
                    else:
                        try:
                            foreign_authors = get_request(node.host + "authors/?page=1&size=2", node)
                        except json.JSONDecodeError:
                            None
                        else:
                            if isinstance(foreign_authors, dict):
                                foreign_author_list = foreign_authors['items']
                            else:
                                foreign_author_list = foreign_authors

                            for author in foreign_author_list:
                                try:
                                    author_posts = get_request(author['id'] + "/posts/", node)
                                except json.JSONDecodeError:
                                    None
                                else:
                                    if isinstance(author_posts, dict):
                                        all_authors_posts.extend(author_posts['items'])
                                    else:
                                        all_authors_posts.extend(author_posts)

                for post in all_authors_posts:
                    print("PPPPPPPPPPPPPPP")
                    print(post)
                    if post['unlisted'] == True: 
                        if request.user.profile.url == post['author']['url']:
                            print("Heeee")
                            viewable_posts.append(post)
                    elif post['visibility'] == "PUBLIC" and post['unlisted'] == False:
                        viewable_posts.append(post)
                    elif post['visibility'] == "FRIENDS" and post['unlisted'] == False:
                        if author_profile.friend_list.filter(id=post['author']['id']).exists() or author_profile.url == post['author']['id']:
                            viewable_posts.append(post)

                friend_posts = Post.objects.none()
                my_friends = author_profile.friends.all()

                for profile in my_friends:
                    friend_posts |= Post.objects.filter(visibility='FRIENDS', author=profile)

                current_user_posts = (public_posts | friend_posts).order_by("-pub_date")
                # print("HAHA: ", current_user_posts[0].visibility,current_user_posts[0].text_post )
         

        # else:
            #  posts = Post.objects.filter(is_public=True).order_by("-pub_date")
            
        all_authors = []
        nodes = Node.objects.all()
        for node in nodes:
            res = requests.get(node.host + "authors/", auth=HTTPBasicAuth(node.username, node.password))
            foreign_authors = res.json()
            all_authors.extend(foreign_authors['items'])
            
        upload_form = UploadForm()
        

        # date_string = viewable_posts[0]['published']
        # dt = datetime.fromisoformat(date_string[:-1])
        # viewable_posts[0]['published'] = dt

        for post in viewable_posts:
            try:
                date_string = post['published']
                dt = datetime.fromisoformat(date_string[:-1])
                post['published'] = dt
            except ValueError:
                pass

        #return render(request, 'home.html', {"posts":posts, "form":form})
        return render(request, 'home.html', {"posts":viewable_posts, "upload_form":upload_form, "authors":all_authors})
    
def send_unlisted_post(request):
  
    print("share_unlisted_post ")
    post_id = request.POST['post_id']
    print("post_id: ", post_id)
    chosen_author = request.POST['my-option'] #receiver
    print("chosen_author", chosen_author)
    # Send a post to the specified id -> copied
    current_user = request.user.profile
    # actor = ProfileSerializer(current_user).data
    # target_host = chosen_author.split("author/")[0]
    # target_node = Node.objects.get(host=target_host)
    # print("GGGGGGGGGGG", target_host)
    # print("GGGGGGGGGGG", target_node)
    # object = requests.get(id + '/', auth=HTTPBasicAuth(target_node.username, target_node.password))
    # object_json = object.json()
    # data_to_send = {
    #     "type": "post",
    #     "summary":actor['displayName'] + " wants to follow" + object_json['displayName'],
    #     "actor":actor,
    #     "object":object_json
    # }
    return render(request, "send_unlistedpost.html")
        
def clear_inbox(request):
    profile = request.user.profile
    for object in profile.inbox.all():
        object.delete()
    profile.save()
    return redirect("inbox")
def inbox(request):
    #should not repeat this code
    if (request.user.is_authenticated == False):
        return redirect("home")
    
    
    all_authors = []
    nodes = Node.objects.all()
    for node in nodes:
        foreign_authors = get_request(node.host + "authors/", node)
        all_authors.extend(foreign_authors['items'])

    #followRequests = FollowRequest.objects.filter(receiver=request.user)
    #postMessage = Post.objects.filter(reciever = request.user)

    curr_user = request.user.profile

    
    inbox = curr_user.inbox.all()
    #n^2
    for ib in inbox:
        for aa in all_authors:
            if ib.actor == aa['id']:
                ib.name = aa['displayName']
                ib.id = aa['id']
                ib.host = ib.actor.split('authors')[0]
    
    return render(request, 'inbox.html', {"items":inbox})

def authors(request):
    all_authors = []
    nodes = Node.objects.all()
    for node in nodes:
        foreign_authors = get_request(node.host + "authors/", node)
        all_authors.extend(foreign_authors['items'])
    return render(request, 'authors.html', {"authors":all_authors})

def authors_list(request):
    all_authors = []
    nodes = Node.objects.all()
    for node in nodes:
        foreign_authors = get_request(node.host + "authors/", node)
        all_authors.extend(foreign_authors['items'])
    return all_authors

def singlePost(request, author_id, post_id):
    if request.user.is_authenticated:

        post = Post.objects.get(id=post_id)


# def edit_profile(request, id):
#     if request.user.is_authenticated:
#         uuid = id.split("/authors/")[1]
#         profile = Profile.objects.get(id = uuid)
        
        
#         form = SignUpForm(request.POST or None, instance=profile)
#         if request.method == 'POST':
            
#             if form.is_valid():
#                 form.save()

        
#         return render(request, "edit_profile.html", {"profile":profile,"form":form })
#     else:
#         messages.success(request, ("You must be logged in to view this page"))
#         return redirect('home')
        
def profile(request, id):
    if request.user.is_authenticated:
        current_user = request.user.profile
        print("aaaaaaaaaaaaaaaaaaaaaaaa")
        print(current_user)
        print(current_user.id)
        
        host = id.split('authors')[0]
        github = ""
        if host == settings.APP_HTTP + settings.APP_DOMAIN + "/main/api/":
            # This is local
            local = True

            uuid = id.split('authors/')[1]
            profile = Profile.objects.get(id=uuid)

            #friends = profile.friend_list.all()

            github = profile.github

            followers = profile.follower_list.all()
            friends = None
                 
            # current user is viewing his own page     
            if current_user.id == uuid:
                print("current user is viewing his own page")
                friends = current_user.friend_list.all()
            else:
                for fl in followers:
                    fl.uuid = fl.id.split('authors/')[1]
                    # current user is in this user follower list
                    if current_user.id == fl.uuid:
                        print("current user is in this user follower list")
                        print(followers)
                        print(fl)
                        print(Follower.objects.get(id=current_user.url, host=host))
                        try:
                            follower = Follower.objects.get(id=current_user.url, host=host)
                            profile.friend_list.add(follower)
                            print("AA")
                            friends = profile.friend_list.all()
                            print(friends)
                        except Follower.DoesNotExist:
                            # If the follower doesn't exist, create a new one
                            follower = Follower.objects.create(id=current_user.url, host=host)
                            profile.friend_list.add(follower)
                            print("BB")
                            friends = profile.friend_list.all()
                        
                    else:
                        print("Unknown error if-else in def profile")
            
            author_node = Node.objects.get(host=host)

            post_list = get_request(id + '/posts/', author_node)

            if request.user.profile.id == id:
                can_follow = False
            else:
                can_follow = True
                
            if friends is not None:
                for fr in friends:
                    temp_profile = Profile.objects.filter(url=fr.id)[0]
                    fr.displayName = temp_profile.displayName
            else:
                friends = None
                
            for fl in followers:
                temp_profile = Profile.objects.filter(url=fl.id)[0]
                fl.displayName = temp_profile.displayName

                if (fl.id == request.user.profile.url):
                    can_follow = False
                    
        else:
            # This is remote
            local = False
            can_follow = True

            if "/api" in host:
                author_node = Node.objects.get(host=host)
            else:
                host = host+"api/"
                author_node = Node.objects.get(host=host)

            author_id = host + "authors/" + id.split('authors/')[1] + "/"

            profile = get_request(author_id, author_node)
            post_json = get_request(author_id + 'posts/', author_node)
            github = profile['github']
            followers = None
            # friends = None

            post_list = []

            if isinstance(post_json, dict):
                post_list = post_json['items']
            else:
                post_list = post_json

            #should not repeat this code
            all_authors = []
            nodes = Node.objects.all()
            for node in nodes:
                foreign_authors = get_request(node.host + "authors/", node)
                all_authors.extend(foreign_authors['items'])

            this_user_id = profile['id']
            
            # current_user = request.user.profile
            # user_this_page = Profile.objects.get(url=this_user_id)
            # print("lllll")
            # print(user_this_page)
        
        #profile github

        if github != "":
            github_username = github.split(".com/")[1]
            url = f"https://api.github.com/users/{github_username}/events"
            response = requests.get(url)
            events = response.json()
        else:
            events = None

        for post in post_list:
            try:
                date_string = post['published']
                dt = datetime.fromisoformat(date_string[:-1])
                post['published'] = dt
            except ValueError:
                pass
        
        return render(request, "profile.html", {"events": events,"profile":profile, "posts":post_list, "friends":friends, "followers":followers, "can_follow": can_follow, "is_local":local})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')


def user_profile(request, id):
    if request.user.is_authenticated:
        profile = Profile.objects.get(id = id)

        return render(request, "profile.html", {"profile":profile})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

def follow(request, id):
    # Send a follow request to the specified id
    current_user = request.user.profile
    actor = ProfileSerializer(current_user).data
    host = id.split("authors")[0]
    if "/api" in host:
        target_host = host
    else:
        target_host = host + "api/"

    target_id = target_host + "authors/" + id.split("authors/")[1] + "/"
    target_node = Node.objects.get(host=target_host)
    object_json = get_request(target_id, target_node)
    data_to_send = {
        "type": "Follow",
        "summary":actor['displayName'] + " wants to follow" + object_json['displayName'],
        "actor":actor,
        "object":object_json
    }
    
    post_request(target_id + "inbox/", target_node, data_to_send)

    return render(request, "follow.html")
    # return render(request, 'home.html', {"display_name": displayName, "actor": actor})


def follow_response(request):
    print("in follow_response")
    if request.user.is_authenticated:
        if request.method == "POST":
            current_user = request.user.profile
            action = request.POST['accept']
            follower_id = request.POST['follower_id']
            following_user = Profile.objects.get(url=follower_id)
            print(current_user)
            print(following_user)

            follower_host = request.POST['follower_host']

            author_node = Node.objects.get(host=follower_host)
            print("JSON: ", follower_id)

            follow_request = Object.objects.get(actor=follower_id, object=current_user.url)

            if action == "accept" or action == "decline":
                current_user.inbox.remove(follow_request)
                follow_request.delete()

            if action == "accept":
                print("in accept")

                # current_user.friend_list.clear()
                # s = Follower.objects.all().delete()
                # f = Object.objects.all().delete()
                # following_user.friend_list.clear()
                # following_user.follower_list.clear()
                # follower_list = current_user.follower_list.all()

                # accept and add follower into your list
                try:
                    follower = Follower.objects.get(id=follower_id, host=follower_host)
                    current_user.follower_list.add(follower)
                except Follower.DoesNotExist:
                    # If the follower doesn't exist, create a new one
                    follower = Follower.objects.create(id=follower_id, host=follower_host)
                    current_user.follower_list.add(follower)
                else:
                    print("Unknown error")

                followers_object = get_request(follower_id + '/followers/', author_node)
                # check before adding to friend list
                for follower in followers_object['items']:
                    if follower['id'] == current_user.url:
                        print("FOUND")
                        friends_to_current_user = Follower.objects.get(id=follower_id)
                        current_user.friend_list.add(friends_to_current_user)

                        # friends_to_following_user = Follower.objects.get(id=current_user.url)
                        # following_user.friend_list.add(friends_to_following_user)

            elif action == "decline":
                # declined dont do anything
                print("in decline dont do anything")

        return redirect(inbox)
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



################################################################################################################################################################

class NodePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='node').exists():
            return True
        return False
  

# TODO: add nodepermission to all remote api requests

class customPaginator(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response(data)



class AuthorList(APIView):
    permission_classes = [NodePermission, IsAuthenticated]
    # queryset = Profile.objects.all()

  
    def get(self, request):
        
        profiles = Profile.objects.all()
        paginator= customPaginator()
        paginated = paginator.paginate_queryset(profiles, request)
        serializer = ProfileSerializer(paginated, many=True)
        updated_data = {"type": "authors", "items": serializer.data}
        return Response(updated_data, status=status.HTTP_200_OK)




class SingleAuthor(APIView):
    permission_classes = [NodePermission, IsAuthenticated]
    def get(self, request, id):
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
        serializer = ProfileSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''api/authors/<str:id>/posts/'''

class PostsList(ListCreateAPIView):
    permission_classes = [NodePermission, IsAuthenticated]

    pagination_class = customPaginator
    serializer_class = PostsSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = "id"

    def get_queryset(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
        profile_instance = Profile.objects.get(id=id)

        posts = Post.objects.filter(author_id=id).all()
        return posts

    def perform_create(self, serializer):

        id = self.kwargs.get(self.lookup_url_kwarg)
        #uri = request.build_absolute_uri('?')
        # profile_id = id

        
        profile_instance = Profile.objects.get(id=id)

        uniqueID = uuid.uuid4()
        post_id = str(uniqueID)

        post = serializer.save(id=post_id,author=profile_instance,content=self.request.data["content"])
        return post
    



'''api/authors/<str:id>/posts/<str:pid>'''
class SinglePost(GenericAPIView):
    permission_classes = [NodePermission, IsAuthenticated]

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = "id"


    def get(self, request, id, pid):
        # uri = request.build_absolute_uri('?')
        posts = Post.objects.get(id=pid)
        serializer = PostSerializer(posts)

        # print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, id, pid):
        uri = request.build_absolute_uri('?')
        try:
            postobj = Post.objects.get(id=pid)
        except postobj.DoesNotExist:
            raise Http404
        serializer = PostSerializer(postobj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, pid):
        uri = request.build_absolute_uri('?')
        if Post.objects.filter(id=pid).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            post_data = request.data
            # author_id = post_data['author']['id']
            # author_uuid = author_id.split('authors/')[1]
            author = Profile.objects.get(id=id)
            Post.objects.create(
                id=pid,
                title=post_data['title'],
                source=post_data['source'],
                origin=post_data['origin'],
                description=post_data['description'],
                contentType=post_data['contentType'],
                content=post_data['content'],
                author=author,
                comments=settings.APP_HTTP+settings.APP_DOMAIN+"/main/api/authors/"+id+"/posts/"+pid+"/comments/"
            )
            return Response(status=status.HTTP_200_OK)


    def delete(self, request, id, pid):
        uri = request.build_absolute_uri('?')
        Post.objects.get(id=pid).delete()
        return Response(status=status.HTTP_200_OK)


'''api/authors/<str:id>/posts/<str:pid>/image'''

class ImagePostsList(APIView):
    permission_classes = [NodePermission, IsAuthenticated]
    # serializer_class = PostImageSerializer
    # queryset = Post.objects.all()
    # lookup_url_kwarg = "id"

    def get(self, request,id,pid):
        
        post = Post.objects.get(id=pid)
        
        # serializer = PostImageSerializer(post)
        try:
             if (post.contentType == "image/png;base64") or (post.contentType == "image/jpeg;base64") or (post.contentType == "application/base64"):
                 return render(request, 'singleImage.html', {"mypost":post})
        except:
            raise Http404
        
       

class FollowerList(APIView):
    permission_classes = [NodePermission, IsAuthenticated]
    def get(self, request, id):

        author = Profile.objects.get(id=id)
        
        serializer = FollowerSerializer(author)
        print("AUTHOR: ", author, "SERIALIZER: ", serializer)
        updated_data = serializer.data
        return Response(updated_data, status=status.HTTP_200_OK)


class singleFollowerList(APIView):
    '''
    Check if foreign id is a follower of this author
    '''
    permission_classes = [NodePermission, IsAuthenticated]
    def get(self, request, id, fid):
        foreign_id = urllib.parse.unquote(fid)
        author = Profile.objects.get(id=id)

        if author.follower_list.filter(id=foreign_id).exists():
            data = {
                "follower":"true"
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "follower":"false"
            }
            return Response(data, status=status.HTTP_200_OK)

    def post(self, request, id, fid):
        foreign_id = urllib.parse.unquote(fid)
        foreign_host = foreign_id.split('authors')[0]
        author = Profile.objects.get(id=id)

        if author.follower_list.filter(id=foreign_id).exists():
            # already a follower, do nothing
            return Response(status=status.HTTP_200_OK)
        else:
            author.follower_list.create(id=foreign_id, host=foreign_host)
            author.save()
            return Response(status=status.HTTP_200_OK)

    def delete(self, request, id, fid):
        foreign_id = urllib.parse.unquote(fid)
        foreign_host = foreign_id.split('/authors')[0]
        author = Profile.objects.get(id=id)

        if author.follower_list.filter(id=foreign_id).exists():
            # Delete the follower from the list
            follower_object = author.follower_list.get(id=foreign_id)
            author.follower_list.remove(follower_object)
            author.save()
            return Response(status=status.HTTP_200_OK)
        else:
            # do nothing
            return Response(status=status.HTTP_200_OK)


class Commentlist(APIView):
    permission_classes = [NodePermission, IsAuthenticated]
    def get(self, request, id, pid):
        post = Post.objects.get(id=pid)
        serializer = CommentListSerializer(post)

        # print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,id,pid):
        # TODO: Add this
        return Response(status=status.HTTP_200_OK)


class postLikes(APIView):
    permission_classes = [NodePermission, IsAuthenticated]
    def get(self, request, id,pid):
        post = Post.objects.get(id=pid)
        serializer = PostLikeSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class commentLikes(APIView):
    permission_classes = [NodePermission, IsAuthenticated]
    def get(self,request,id,pid,cid):
        comment = Comment.objects.get(id=cid)
        serializer = CommentLikeSerializer(comment)

        return Response(serializer.data, status=status.HTTP_200_OK)


class authorLikes(APIView):
    permission_classes = [NodePermission, IsAuthenticated]
    def get(self,request,id):
        author = Profile.objects.get(id=id)
        serializer = AuthorLikeSerializer(author)

        return Response(serializer.data, status=status.HTTP_200_OK)


class InboxList(APIView):
    permission_classes = [NodePermission, IsAuthenticated]
    def get(self,request,id):
        profile = Profile.objects.get(id=id)
        serializer = InboxSerializer(profile)
        updated_data = serializer.data

        return Response(updated_data, status=status.HTTP_200_OK)

    def post(self,request,id):
        profile = Profile.objects.get(id=id)
        data = request.data
        type = data["type"]

        if (type == "Follow") or (type == "follow"):
            print("Trying to make follow request")
            try:
                object = Object.objects.get(actor=data["actor"]["id"],object=data["object"]["id"])
                print("We found the object")
                profile.inbox.add(object)
            except Object.DoesNotExist:
                print("we didn't get the object")
                # If the follower doesn't exist, create a new one
                object = Object.objects.create(
                    type="Follow",
                    actor=data["actor"]["id"],
                    object=data["object"]["id"],
                )
                profile.inbox.add(object)
            else:
                print("Unknown error")

            profile.save()
            return Response(status=status.HTTP_200_OK)

        elif (type == "post") or (type == "Post"):
            object = Object.objects.create(
                type="post",
                object_id=data["id"],
                actor=data["author"]["id"]
            )
            profile.inbox.add(object)
            profile.save()
            return Response(status=status.HTTP_200_OK)

        elif (type == "Like") or (type == "like"):
            isComment = False
            if "/comments/" in data["object"]:
                isComment = True
            object = Object.objects.create(
                type="like",
                object_id=data["object"],
                actor = data["author"]["id"],
                whether_comment_like=isComment
            )
            profile.inbox.add(object)
            profile.save()
            like = Like.objects.create(
                object_id=data["object"],
                author_id=data["author"]["id"]
            )

            # If the like is for a post, create a like object and add it to that post's likes
            split_id = data["object"].split("/")
            object_type = split_id[len(split_id) - 3]
            id = split_id[len(split_id) - 2]
            if object_type == "posts":
                post = Post.objects.get(id=id)
                post.likes.add(like)

            elif object_type == "comments":
                comment = Comment.objects.get(id=id)
                comment.likes.add(like)

        elif (type == "comment") or (type == "Comment"):
            object = Object.objects.create(
                type="comment",
                object_id=data["id"],
                actor = data["author"]["id"]
            )
            profile.inbox.add(object)
            profile.save()

            print(data["author"]["id"])

            comment = Comment.objects.create(
                comment=data["comment"],
                author_id=data["author"]["id"],
                id=data["id"],
                created_at=data["published"],
            )

            # store comment on the post
            post_url = data["id"].split("/comments")[0]
            post_id = post_url.split("posts/")[1]
            post = Post.objects.get(id=post_id)
            post.comments.add(comment)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    def delete(self,request,id):
        # clear the inbox
        profile = Profile.objects.get(id=id)
        for object in profile.inbox.all():
            object.delete()
        profile.save()

        return Response(status=status.HTTP_200_OK)