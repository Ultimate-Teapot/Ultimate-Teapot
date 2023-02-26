from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Post, Author


class PostForm(forms.ModelForm):
    text = forms.CharField(required=True, 
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
        exclude = ("user", "visibility", "likes")

class AuthorCreationForm(UserCreationForm):

    class Meta:
        model = Author
        fields = ("username", "password")

    def save(self, commit=True):
        user = super(AuthorCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class AuthorChangeForm(UserChangeForm):

    class Meta:
        model = Author
        fields = ("username", "password")