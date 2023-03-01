from django import forms
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
        exclude = ("user", "visibility", "likes")
