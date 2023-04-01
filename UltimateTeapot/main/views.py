import base64
import datetime
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
from .paginations import NewPaginator
import base64
from django.core.files.base import ContentFile



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

def foreign_post(request, id):
    # Pass in the full URL of a post, make a get request and display it on a page
    # Make comments
    comment_form = CommentForm(request.POST or None)

    host = id.split("authors")[0]
    node = Node.objects.get(host=host)
    post_obj = requests.get(id + "/", auth=HTTPBasicAuth(node.username, node.password))
    post_json = post_obj.json()

    post_comments = requests.get(id + "/comments/", auth=HTTPBasicAuth(node.username, node.password))
    post_comments_json = post_comments.json()

    return render(request, "foreign_post.html", {"post":post_json, "comments":post_comments_json['comments'], "comment_form":comment_form})


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

def delete_post(request, id):
    post = Post.objects.get(id = id)
    post.delete()
    return redirect('home')

def edit_post(request, id):
    post = Post.objects.get(id = id)
    form = UploadForm(request.POST or None, instance=post)
    if request.method == "POST":
        if form.is_valid():      
            form.save()
            messages.success(request, ("You Successfully Edited!"))
            return redirect('home')
    #upload_form = UploadForm()
    post.delete()
    return render(request, "edit_post.html", {"post":post, "upload_form":form})


        




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
            #image = request.FILES.get('image')

            contentType = request.POST['contentType']
            image = request.FILES.get('image')


            # See what to set content type to #
            if image:
                try:
                    if ".png" in image.name:
                        contentType = "image/png;base64"
                    if (".jpeg" in image.name) or (".jpg" in image.name):
                        contentType = "image/jpeg;base64"
                except:
                    contentType = "application/base64"
             

            if contentType == ("image/png;base64") or ("image/jpeg;base64") or ("application/base64"):
                image = request.FILES.get('image')
                b_64 = base64.b64encode(image.file.read())
                content = b_64
            else:
                content = request.POST['content']
            
            


            visibility = request.POST['visibility']
            title = request.POST['title']
            if ('unlisted' in request.POST):
                unlisted = request.POST['unlisted']
            else:
                unlisted = False
            if (unlisted == 'on'):
                unlisted = True

            new_post = Post.objects.create(title=title,id=post_id, author=author_profile, content=content,
                                           visibility=visibility, unlisted=unlisted,contentType=contentType,image=image)
            new_post.save()

        # return redirect('home')
        # return render(request, 'home.html', {"upload_form":upload_form})
    # else:
    #     #return redirect('home')
    #     upload_form = UploadForm()

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
            requests.post(author_id + "/inbox/", json=obj_json, auth=HTTPBasicAuth(node.username, node.password))


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
        requests.post(author_id + "/inbox/", json=obj_json, auth=HTTPBasicAuth(node.username, node.password))


    return redirect('foreign_post', id)

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
                # if form.data['image'] is not None:
                #     form.contentType = "application/base64"
                
                # if form.data['content'] is not None:
                #     form.contentType = "text/plain"

                # if form.data['markdown_content'] is not None:
                #     form.contentType = "text/markdown"

                
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
         
        # else:
            #  posts = Post.objects.filter(is_public=True).order_by("-pub_date")
        upload_form = UploadForm()
        #return render(request, 'home.html', {"posts":posts, "form":form})
        return render(request, 'home.html', {"posts":current_user_posts, "upload_form":upload_form})


def inbox(request):
    
    #followRequests = FollowRequest.objects.filter(receiver=request.user)
    #postMessage = Post.objects.filter(reciever = request.user)

    curr_user = request.user.profile
    inbox = curr_user.inbox.all()


    return render(request, 'inbox.html', {"items":inbox})

def authors(request):
    all_authors = []

    nodes = Node.objects.all()
    for node in nodes:
        res = requests.get(node.host + "authors/", auth=HTTPBasicAuth(node.username, node.password))
        foreign_authors = res.json()
        all_authors.extend(foreign_authors['items'])

    return render(request, 'authors.html', {"authors":all_authors})

def singlePost(request, author_id, post_id):
    if request.user.is_authenticated:

        post = Post.objects.get(id=post_id)



def profile(request, id):
    if request.user.is_authenticated:
        host = id.split('authors')[0]
        author_node = Node.objects.get(host=host)

        author_object = requests.get(id + '/', auth=HTTPBasicAuth(author_node.username, author_node.password))
        posts = requests.get(id + '/posts/', auth=HTTPBasicAuth(author_node.username, author_node.password))
        print(posts)
        post_json = posts.json()
        post_list = []

        if isinstance(post_json, dict):
            post_list = post_json['items']
        else:
            post_list = post_json

        # if request.method == "POST":
        #     current_user_id = request.user.profile.id
        #
        #     action = request.POST['follow']
        #     if action == "follow":
        #         # profile.followers.add(current_user)
        #         #
        #         # if current_user in profile.users_following.all():
        #         #     profile.friends.add(current_user)
        #         #     current_user.friends.add(profile)
        #         if not FollowRequest.objects.filter(sender=request.user, receiver=profile.user).exists():
        #             FollowRequest.objects.create(sender=request.user, receiver=profile.user)
        #
        #     elif action == "unfollow":
        #         profile.followers.remove(current_user)
        #         if current_user in profile.friends.all():
        #             profile.friends.remove(current_user)
        #             current_user.friends.remove(profile)
        #
        #     profile.save()

        return render(request, "profile.html", {"profile":author_object.json(), "posts":post_list})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

def follow(request, id):
    # Send a follow request to the specified id
    current_user = request.user.profile
    actor = ProfileSerializer(current_user).data
    target_host = id.split("author")[0]
    target_node = Node.objects.get(host=target_host)
    object = requests.get(id + '/', auth=HTTPBasicAuth(target_node.username, target_node.password))
    object_json = object.json()

    data_to_send = {
        "type": "Follow",
        "summary":actor['displayName'] + " wants to follow" + object_json['displayName'],
        "actor":actor,
        "object":object_json
    }

    requests.post(id + "/inbox/", json=data_to_send, auth=HTTPBasicAuth(target_node.username, target_node.password))

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

class AuthorList(APIView):
    # permission_classes = [NodePermission, IsAuthenticated]

    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        updated_data = {"type": "authors", "items": serializer.data}

        return Response(updated_data, status=status.HTTP_200_OK)


class SingleAuthor(APIView):
    # permission_classes = [NodePermission, IsAuthenticated]
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
        serializer = ProfileSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''api/authors/<str:id>/posts/'''

class PostsList(ListCreateAPIView):
    # permission_classes = [NodePermission, IsAuthenticated]

    pagination_class = NewPaginator
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
   #permission_classes = [NodePermission, IsAuthenticated]

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
        # try:
        #     postobj = Post.objects.get(id=pid)
        # except postobj.DoesNotExist:
        #     serializer = PostSerializer(postobj,data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data)
        # else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
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

class ImagePostsList(GenericAPIView):
    serializer_class = PostImageSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = "id"

 # TODO check if this works
    def get(self, request, id, pid):
        # uri = request.build_absolute_uri('?')
        post = Post.objects.get(id=pid)
        serializer = PostImageSerializer(post)
        if(post.contentType!="application/base64"):
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowerList(APIView):
    def get(self, request, id):
        #uri = request.build_absolute_uri('?')
        #uri = uri.replace("/followers", "")

        author = Profile.objects.get(id=id)
        serializer = FollowerSerializer(author)
        updated_data = serializer.data
        return Response(updated_data, status=status.HTTP_200_OK)


class singleFollowerList(APIView):
    '''
    Check if foreign id is a follower of this author
    '''
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
    def get(self, request, id, pid):
        post = Post.objects.get(id=pid)
        serializer = CommentListSerializer(post)

        # print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,id,pid):
        # TODO: Add this
        return Response(status=status.HTTP_200_OK)


class postLikes(APIView):
    def get(self, request, id,pid):
        post = Post.objects.get(id=pid)
        serializer = PostLikeSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

class commentLikes(APIView):
    def get(self,request,id,pid,cid):
        comment = Comment.objects.get(id=cid)
        serializer = CommentLikeSerializer(comment)

        return Response(serializer.data, status=status.HTTP_200_OK)


class authorLikes(APIView):
    def get(self,request,id):
        author = Profile.objects.get(id=id)
        serializer = AuthorLikeSerializer(author)

        return Response(serializer.data, status=status.HTTP_200_OK)


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

        if (type == "Follow") or (type == "follow"):
            object = Object.objects.create(
                type="Follow",
                actor=data["actor"]["id"],
                object=data["object"]["id"],
            )
            profile.inbox.add(object)
            profile.save()
            return Response(status=status.HTTP_200_OK)

        elif (type == "post") or (type == "Post"):
            object = Object.objects.create(
                type="post",
                object_id=data["id"]
            )
            profile.inbox.add(object)
            profile.save()
            return Response(status=status.HTTP_200_OK)

        elif (type == "Like") or (type == "like"):
            object = Object.objects.create(
                type="like",
                object_id=data["object"]
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
                object_id=data["id"]
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