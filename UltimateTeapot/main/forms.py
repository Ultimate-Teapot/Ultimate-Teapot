from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Post, Profile

POST_TYPE = [
    (0, 'Private (Only you can see)'),
    (1, 'Public (Everyone can see)'),
    (2, 'Private (Only your friends can see)'),
    (3, 'Private (Only people you send this post can see)'),
    (4, 'Unlisted (Only accessible via link)')
]
  
class UploadForm(forms.ModelForm):
    
    text_post = forms.CharField(required=True, 
        widget= forms.widgets.Textarea(
            attrs = {
                "placeholder": "Enter Your Thoughts!",
                "class": "form-control",
            }
            ),
            label = "",
        )
    post_type = forms.CharField(label='Who would you like to share your post?', widget=forms.RadioSelect(choices=POST_TYPE))
    # current_user = User.objects.get(username=)
    # author_profile = Profile.objects.get(user=current_user)
    # friends_to_choose = forms.ModelChoiceField(queryset=author_profile.friends.all(), widget=forms.CheckboxSelectMultiple) 
    
    class Meta:
        model = Post
        fields = ('text_post', 'image', 'post_type',)
        #labels = {'is_public': 'Make post public?'}
        
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop("request") # store value of request 
    #     print(self.request.user) 
    #     super().__init__(*args, **kwargs)

    #is_public = forms.BooleanField(required=False)
    
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
        
        
