from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('signup', views.signup, name='signup'),
  path('signin', views.signin, name='signin'),
  path('logout', views.logout, name='logout'),
  path('home/', views.home, name="home"),
  #path('', views.index, name='index'),
  path('posts/', views.posts, name='posts'),
  path('authors/', views.authors, name='authors')
]