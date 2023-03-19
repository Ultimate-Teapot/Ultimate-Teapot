from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Post

class UploadForm(forms.ModelForm):
    text_post = forms.CharField(required=True, 
        widget=forms.widgets.Textarea(
            attrs = {
                "placeholder": "Enter Your Thoughts!",
                "class": "form-control",
            }
            ),
            label = "",
        )
    class Meta:
        model = Post
        fields = ('text_post', 'image', 'is_public',)
        labels = {'is_public': 'Make post public?'}

    is_public = forms.BooleanField(required=False)
    
# class PostForm(forms.ModelForm):
#     text = forms.CharField(required=True, 
#         widget=forms.widgets.Textarea(
#             attrs = {
#                 "placeholder": "Enter Your Thoughts!",
#                 "class": "form-control",
#             }
#             ),
#             label = "",
#         )
    
#     class Meta:
#         model = Post
#         fields = ('text', 'image', 'pub_date', 'post_id', 'author')
#         exclude = ("user", "visibility", "likes")

#if needed extra fields for sign up form
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True,)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email',)
        #fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
        
