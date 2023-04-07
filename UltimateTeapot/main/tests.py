from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Post
from django.test import Client
from django.db import IntegrityError


# This snippet of code was taken from here:
        # Source: https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
        # Author: dmrz
        # Date: Jul 13, 2017
import datetime
from django.conf import settings
from django.utils.timezone import make_aware

 

# at the moment these tests will only run at this base url -> http://127.0.0.1:8000/

'''class CreateUserTestCase(TestCase):
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
        

        newpost = Post.objects.create(post_id = "1",author=profile, text="hello world I am a camel",pub_date=aware_datetime)
        newpost.save()
        mypost = Post.objects.get(post_id="1")

        assert(mypost.text=="hello world I am a camel")


    # Test to see whether we can signup a user
    def test_Sign_Up(self):

        client = Client()
        data = {'username':'camelCase','email':'camel@desert.com','password':'chicken','confirmpassword':'chicken'}
        response = client.post('http://127.0.0.1:8000/main/signup', data)
        
        
        self.assertEqual(response.status_code, 302) # if 302 it is a sucessful redirect

    

    def test_Log_In(self):

        client = Client()
        data = {'username':'camelCase','email':'camel@desert.com','password':'chicken','confirmpassword':'chicken'}
        client.post('http://127.0.0.1:8000/main/signup', data)
        

        data1 = {'username': 'camelCase', 'password': 'chicken'}
        response = client.post('http://127.0.0.1:8000/main/login/', data1)
        self.assertEqual(response.status_code, 302) # if 302 it is a sucessful redirect




    def test_get_profile(self):

        newUser = User.objects.create_user(username="camelCase", email="camel@desert.com", password="chicken", first_name = "crazy", last_name = "camel")
        newUser.save()
        new_profile = Profile.objects.create(user=newUser)
        new_profile.save()
       
        client = Client()
        client.post('http://127.0.0.1:8000/main/login/', {'username': 'camelCase', 'password': 'chicken'})
        response = client.get('http://127.0.0.1:8000/main/authors/camelCase')
        self.assertEqual(response.status_code, 200) 


    def test_follow(self):


        client = Client()

        newUser = User.objects.create_user(username="snakecase", email="snake@desert.com", password="duck", first_name = "sneaky", last_name = "snake")
        newUser.save()
        new_profile = Profile.objects.create(user=newUser)
        new_profile.save()

        # register camelCase
        data = {'username':'camelCase','email':'camel@desert.com','password':'chicken','confirmpassword':'chicken'}
        client.post('http://127.0.0.1:8000/main/signup', data)
        
        # login to camelCase
        data1 = {'username': 'camelCase', 'password': 'chicken'}
        client.post('http://127.0.0.1:8000/main/login/', data1)


        # This will get the user and follow then unfollow them
        client.get('http://127.0.0.1:8000/main/authors/')
        client.get('http://127.0.0.1:8000/main/authors/snakecase')
        response1=client.post('http://127.0.0.1:8000/main/authors/snakecase',{"follow":"unfollow"})
        response=client.post('http://127.0.0.1:8000/main/authors/snakecase',{"follow":"unfollow"})

        self.assertEqual(response1.status_code, 200) 
        self.assertEqual(response.status_code, 200) 


        # run tests using  python manage.py tests
        #Tests to add 
        #Test posting'''


        

   