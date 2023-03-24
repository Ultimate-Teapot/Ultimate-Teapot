from django.urls import path,include
from . import views
from .views import AuthorList, SingleAuthor, PostsList, SinglePost, FollowerList, Commentlist


# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'apiprofile', views.ProfileViewSet)
# router.register(r'apiposts', views.PostViewSet)
# router.register(r'apiusers',views.UserViewSet)


urlpatterns = [
  path('', views.home, name='home'),
  path('signup', views.signup, name='signup'),
  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
  path('posts', views.posts, name='posts'),
  path('posts/<str:id>', views.post, name='post'),
  path('like', views.like, name='like'),
  path('home/', views.home, name="home"),
  path('<str:post_id>/like/', views.like_create, name='like_create'),
  path('authors/<str:id>/posts/<str:post_id>/comment/', views.comment_create, name='comment_create'),
  #path('', views.index, name='index'),
  #path('posts/', views.posts, name='posts'),
  path('authors/', views.authors, name='authors'),
  path('authors/<str:id>', views.profile, name='profile'),
  path('inbox/', views.inbox, name='inbox'),

  
#--- below for the rest frame work ---#
  # path('', include(router.urls)),
  # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

  path('api/authors/', AuthorList.as_view(), name='authors_api'),
  path('api/authors/<str:id>', SingleAuthor.as_view(), name='author_api'),
  path('api/authors/<str:id>/followers', FollowerList.as_view(), name='followers_api'),
  path('api/authors/<str:id>/posts/', PostsList.as_view(), name='posts_api'),
  path('api/authors/<str:id>/posts/<str:pid>', SinglePost.as_view(), name='post_api'),
  path('api/authors/<str:id>/posts/<str:pid>/comments', Commentlist.as_view(), name='post_api'),
]