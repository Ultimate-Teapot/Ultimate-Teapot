from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Post, Comment, Profile, Like, Node, Object, Follower

class ProfileInLine(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInLine]

admin.site.register
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Node)
admin.site.register(Object)
admin.site.register(Follower)

