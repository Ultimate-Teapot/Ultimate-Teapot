from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Post
from django.test import Client
#import datetime
from django.db import IntegrityError



class CreateUserTestCase(TestCase):
    def test_create_user(self):
        

        newUser = User.objects.create_user(username="camelCase", email="camel@desert.com", password="chicken", first_name = "crazy", last_name = "camel")
        newUser.save()
        
        
        new_profile = Profile.objects.create(user=newUser)
        new_profile.save()

        new_user = User.objects.get(username="camelCase")
        profile = Profile.objects.get(user=new_user)
        profile.follower_num=5

        print(profile.follower_num)

        assert(new_user.get_full_name()=="crazy camel")


    def test_duplicate_user(self):
        try:
            newUser = User.objects.create_user(username="camelCase", email="camel@desert.com", password="chicken", first_name = "crazy", last_name = "camel")
            newUser.save()
            newUser = User.objects.create_user(username="camelCase", email="camel@desert.com", password="chicken", first_name = "crazy", last_name = "camel")
            newUser.save()
    
        
        except IntegrityError:
            assert(1==1)


    def test_post(self):
      
        # Maybe create one for if no user exists?
        newUser = User.objects.create_user(username="camelCase", email="camel@desert.com", password="chicken", first_name = "crazy", last_name = "camel")
        newUser.save()
        new_profile = Profile.objects.create(user=newUser)
        new_profile.save()

        new_user = User.objects.get(username="camelCase")
        profile = Profile.objects.get(user=new_user)

        newpost = Post.objects.create(post_id = "1",author=profile, text="hello world I am a camel",pub_date='2022-10-25 14:49:30')
        newpost.save()
        mypost = Post.objects.get(post_id="1")

        assert(mypost.text=="hello world I am a camel")

    


        # run tests using  python manage.py tests
        # def test_create_user(self):

        # def test_create_user(self):


        # Tests to add
        # Test login 
        # Test Signup
        # Test 

   