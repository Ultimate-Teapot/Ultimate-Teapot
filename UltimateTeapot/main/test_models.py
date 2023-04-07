from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Like
from django.test import Client
from django.db import IntegrityError
from main.forms import SignUpForm


# This snippet of code was taken from here:
        # Source: https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
        # Author: dmrz
        # Date: Jul 13, 2017
import datetime
from django.conf import settings
from django.utils.timezone import make_aware

 

# at the moment these tests will only run at this base url -> http://127.0.0.1:8000/

class CreateUserTestCase(TestCase):
    def test_create_user_db(self):
        

        newUser = User.objects.create_user(username="camelCase", email="camel@desert.com", password="chicken", first_name = "crazy", last_name = "camel")
        newUser.save()
        
        
        new_profile = Profile.objects.create(user=newUser)
        new_profile.save()

        new_user = User.objects.get(username="camelCase")
        
        assert(new_user.get_full_name()=="crazy camel")
        


    def test_duplicate_user_db(self):
        try:
            newUser = User.objects.create_user(username="camelCase", email="camel@desert.com", password="chicken", first_name = "crazy", last_name = "camel")
            newUser.save()
            newUser = User.objects.create_user(username="camelCase", email="camel@desert.com", password="chicken", first_name = "crazy", last_name = "camel")
            newUser.save()
    
        
        except IntegrityError:
            assert(1==1)

    


    def test_post_db(self):
      
        # Maybe create one for if no user exists?
        newUser = User.objects.create_user(username="camelCase", email="camel@desert.com", password="chicken", first_name = "crazy", last_name = "camel")
        newUser.save()
        new_profile = Profile.objects.create(user=newUser)
        new_profile.save()

        new_user = User.objects.get(username="camelCase")
        profile = Profile.objects.get(user=new_user)


        # This snippet of code was taken from here:
        # Source: https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
        # Author: dmrz
        # Date: Jul 13, 2017
        naive_datetime = datetime.datetime.now()
        naive_datetime.tzinfo  # None
        settings.TIME_ZONE  # 'UTC'
        aware_datetime = make_aware(naive_datetime)
        

        newpost = Post.objects.create(id = "1",author=profile, content="hello world I am a camel",pub_date=aware_datetime)
        newpost.save()
        mypost = Post.objects.get(id="1")

        assert(mypost.content=="hello world I am a camel")


class CommentTestCase(TestCase):
        def test_comment(self):
             newUser = User.objects.create_user(username="camelCase", email="camel@desert.com", password="chicken", first_name = "crazy", last_name = "camel")
             newUser.save()
             new_profile = Profile.objects.create(user=newUser)
             new_profile.save()

             new_user = User.objects.get(username="camelCase")
             profile = Profile.objects.get(user=new_user)


        # This snippet of code was taken from here:
        # Source: https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
        # Author: dmrz
        # Date: Jul 13, 2017
             naive_datetime = datetime.datetime.now()
             naive_datetime.tzinfo  # None
             settings.TIME_ZONE  # 'UTC'
             aware_datetime = make_aware(naive_datetime)
             newcomment = Comment.objects.create(id = "2",author_id=profile.id, comment="hello world I am a camel",created_at=aware_datetime)
             #newcomment.likes.set(0)
             newcomment.save()
             mycomment = Comment.objects.get(id="2")

             assert(mycomment.comment=="hello world I am a camel")


class LikeTestCase(TestCase):
        def test_comment(self):
            newUser = User.objects.create_user(username="camelCase", email="camel@desert.com", password="chicken", first_name = "crazy", last_name = "camel")
            newUser.save()
            new_profile = Profile.objects.create(user=newUser)
            new_profile.save()

            new_user = User.objects.get(username="camelCase")
            profile = Profile.objects.get(user=new_user)


        # This snippet of code was taken from here:
        # Source: https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
        # Author: dmrz
        # Date: Jul 13, 2017
            naive_datetime = datetime.datetime.now()
            naive_datetime.tzinfo  # None
            settings.TIME_ZONE  # 'UTC'
            aware_datetime = make_aware(naive_datetime)
        

            newpost = Post.objects.create(id = "1",author=profile, content="hello world I am a camel",pub_date=aware_datetime)
            newpost.save()
            mypost = Post.objects.get(id="1")

            naive_datetime = datetime.datetime.now()
            naive_datetime.tzinfo  # None
            settings.TIME_ZONE  # 'UTC'
            aware_datetime = make_aware(naive_datetime)

            newlike = Like.objects.create(object_id="1", author_id=profile.id, created_at=aware_datetime)

            assert(newlike.object_id=="1")



