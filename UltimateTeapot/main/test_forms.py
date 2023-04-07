from django.test import TestCase
from main.forms import SignUpForm, UploadForm, CommentForm
from django.contrib.auth.forms import UserCreationForm

class TestForms(TestCase):
    def setUp(self) -> None:
        self.form_class = SignUpForm
    def test_sign_up(self):
       
        self.assertTrue(issubclass(self.form_class, UserCreationForm))
        self.assertTrue('email' in self.form_class.Meta.fields)
        self.assertTrue('username' in self.form_class.Meta.fields)
        
    def test_upload(self):
        self.form_class = UploadForm
        self.assertTrue('title' in self.form_class.Meta.fields)
        self.assertTrue('content' in self.form_class.Meta.fields)
        self.assertTrue('image' in self.form_class.Meta.fields)
        self.assertTrue('visibility' in self.form_class.Meta.fields)
        self.assertTrue('unlisted' in self.form_class.Meta.fields)
        
    def test_comment(self):
        self.form_class = CommentForm
        self.assertTrue('comment' in self.form_class.Meta.fields)
        



        
        