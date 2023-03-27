from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Post, Comment

VISIBILITY = [
    ('PUBLIC', 'PUBLIC'),
    ('FRIENDS', 'FRIENDS'),
]




class UploadForm(forms.ModelForm):
    content = forms.CharField(required=False,
                              widget=forms.widgets.Textarea(
                                  attrs={
                                      "placeholder": "Enter Your Thoughts!",
                                      "class": "form-control",
                                  }
                              ),
                              label="",
                              )
    # markdown_content = forms.CharField(required=False,
    #                           widget=forms.widgets.Textarea(
    #                           ))
    
    title = forms.CharField()
    visibility = forms.CharField(label='Choose your post visibilty?', widget=forms.RadioSelect(choices=VISIBILITY))
    unlisted = forms.BooleanField(label='Unlisted?', required=False)

    contentType = forms.CharField()

   

    #image = forms.ImageField()
    


    class Meta:
        model = Post
        fields = ('title', 'content','image', 'visibility', 'unlisted','contentType')
        # labels = {'is_public': 'Make post public?'}
        exclude = ("user", "visibility", "likes", 'author')

    # is_public = forms.BooleanField(required=False)
    
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

    display_name = forms.CharField(max_length=100, required=True,)
    github = forms.URLField(max_length=100, required=False,)
    profile_image = forms.URLField(max_length=200, required=False,)
    
    class Meta:
        model = User
        fields = ('username', 'email',)
        #fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )



class CommentForm(forms.ModelForm):
    content = forms.CharField(required=True, 
            widget=forms.widgets.Textarea(
            attrs = {
                "placeholder": "Enter Your Comment!",
                "class": "form-control",
            }
            ),
            label = "",
        )
    class Meta:
        model = Comment
        fields = ['content']