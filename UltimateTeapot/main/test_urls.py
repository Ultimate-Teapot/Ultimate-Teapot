from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import authenticate, login
from main.views import teapot, index, post, foreign_post, delete_post, edit_post, edit_profile, signup,logout, posts, make_comment, like_post, like, myprofile, make_post, home, clear_inbox, inbox, authors, authors_list, singlePost, edit_profile, profile, user_profile, follow, follow_response, comment_create, like_create

class TestUrls(SimpleTestCase):
    def test_clear_inbox_url(self):
        url = reverse('clear_inbox')
        print("Resolve", resolve(url).func)
        self.assertEquals(resolve(url).func, clear_inbox)

    def test_home_url(self):
        url = reverse('home')
        print("Resolve", resolve(url).func)
        self.assertEquals(resolve(url).func, home)


    def test_teapot_url(self):
        url = reverse('teapot')
        self.assertEquals(resolve(url).func, teapot)


    def test_signup_url(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, signup)

    def test_like_url(self):
        url = reverse('like')
        self.assertEquals(resolve(url).func, like)

    def test_posts_url(self):
        url = reverse('posts')
        self.assertEquals(resolve(url).func, posts)

    def test_make_post_url(self):
        url = reverse('make_post')
        self.assertEquals(resolve(url).func, make_post)


    def test_authors_url(self):
        url = reverse('authors')
        self.assertEquals(resolve(url).func, authors)


    def test_inbox_url(self):
        url = reverse('inbox')
        self.assertEquals(resolve(url).func, inbox)

    def test_myprofile_url(self):
        url = reverse('user_profile2')
        self.assertEquals(resolve(url).func, myprofile)

    def test_follow_response_url(self):
        url = reverse('follow_response')
        self.assertEquals(resolve(url).func, follow_response)

