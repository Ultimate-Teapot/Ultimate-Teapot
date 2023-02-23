from django.http import HttpResponse
from .models import Post

def index(request):
    return HttpResponse("Hello, world. You're at the main\ index.")

def posts(request):
    posts = Post.objects.all()

    return HttpResponse( posts)