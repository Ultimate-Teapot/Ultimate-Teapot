from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class CreateUserTestCase(TestCase):
    def test_create_user(self):
        

        newUser = User.objects.create_user(username="camelCase", email="camel@desert.com", password="chicken", first_name = "crazy", last_name = "camel")
        newUser.save()
        
        new_profile = Profile.objects.create(user=newUser)
        new_profile.save()

        new_user = User.objects.get(username="camelCase")
        profile = Profile.objects.get(user=new_user)
        profile.followerno=5

        print(profile.followerno)

        assert(new_user.get_full_name()=="crazy camel")


        # run tests using  python manage.py tests
        # def test_create_user(self):

        # def test_create_user(self):
      
        

        



