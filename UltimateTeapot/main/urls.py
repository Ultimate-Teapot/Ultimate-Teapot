from django.urls import path
from . import views
from .views import ProfileList

urlpatterns = [
  path('', views.home, name='home'),
  path('signup', views.signup, name='signup'),
  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
  path('posts', views.posts, name='posts'),
  path('posts/<str:post_id>', views.post, name='post'),
  path('like', views.like, name='like'),
  path('home/', views.home, name="home"),
  #path('', views.index, name='index'),
  path('authors/', views.authors, name='authors'),
  path('authors/<str:username>', views.profile, name='profile'),
  path('service/authors', ProfileList.as_view(), name='authors_api'),
]