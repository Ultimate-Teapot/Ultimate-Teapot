from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Post

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
        fields = ('text', 'image', 'pub_date', 'post_id', 'author')
        exclude = ("user", "visibility", "likes")
