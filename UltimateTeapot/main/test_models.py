from django.test import TestCase
from main.models import Node, Object, Follower, Like, Profile, FollowRequest, Comment, Post

class TestModels(TestCase):
    def setUp(self):
        self.node1 = Node.objects.create()