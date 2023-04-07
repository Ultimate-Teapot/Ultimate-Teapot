from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Post, Comment, Profile

VISIBILITY = [
    ('PUBLIC', 'PUBLIC'),
    ('FRIENDS', 'FRIENDS'),
]
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('displayName', 'github', 'profileImage')
        
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

    title = forms.CharField()
    visibility = forms.CharField(label='Choose your post visibilty?', widget=forms.RadioSelect(choices=VISIBILITY))
    unlisted = forms.BooleanField(label='Unlisted?', required=False)
    image = forms.ImageField(required=False) #turned of required = False
  

    contentType = forms.CharField(widget=forms.HiddenInput(), required=False)
    #image = forms.ImageField()
    


    class Meta:
        model = Post
        fields = ('title', 'content','image', 'visibility', 'unlisted')
        # labels = {'is_public': 'Make post public?'}
        exclude = ("user", "visibility", "likes", 'author', 'contentType')

    # is_public = forms.BooleanField(required=False)

class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
        attrs={
            "placeholder": "Enter a comment!",
            "class": "form-control",
            }
        ),
        label="",
    )

    class Meta:
        model = Comment
        fields = ('comment',)


#if needed extra fields for sign up form
class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True,)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    display_name = forms.CharField(max_length=100, required=True,)
    github = forms.URLField(max_length=100, required=False,)

    profile_image = forms.URLField(max_length=200, required=False, initial="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")

    

    def clean_field(self):
        data = self.cleaned_data['profile_image']
        if not data:
            data = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
        return data
    class Meta:
        model = User
        fields = ('username', 'email',)
        #fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )




