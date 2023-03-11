from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('signup', views.signup, name='signup'),
  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
  path('home/', views.home, name="home"),
  #path('', views.index, name='index'),
  path('posts/', views.posts, name='posts'),
  path('authors/', views.authors, name='authors'),
  path('authors/<str:username>', views.profile, name='profile'),
  path('inbox/', views.inbox, name='inbox'),
]