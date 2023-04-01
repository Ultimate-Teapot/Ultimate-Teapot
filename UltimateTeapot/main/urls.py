from django.urls import path,include
from . import views
from .views import AuthorList, SingleAuthor, PostsList, SinglePost, FollowerList, Commentlist, singleFollowerList, ImagePostsList, authorLikes,commentLikes,postLikes,InboxList



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
  # path('upload', views.upload, name='upload'),
  path('like', views.like, name='like'),
  path('home/', views.home, name="home"),
  path('<str:post_id>/like/', views.like_create, name='like_create'),
  # ('authors/<str:author_id>')
  path('posts/', views.posts, name='posts'),
  path('posts/<str:id>', views.post, name='post'),
  path('make_comment/<path:id>', views.make_comment, name='make_comment'),
  path('like_post/<path:id>', views.like_post, name='like_post'),
  # For testing posts and comments from other servers
  path('foreign_post/<path:id>/', views.foreign_post, name='foreign_post'),
  path('authors/<str:author_id>/posts/<str:post_id>', views.singlePost, name='singlePost'),
  path('authors/<str:id>/posts/<str:post_id>/comment/', views.comment_create, name='comment_create'),
  # path('', views.index, name='index'),
  # path('posts/', views.posts, name='posts'),
  path('authors/', views.authors, name='authors'),
  path('authors/<path:id>', views.profile, name='profile'),
  path('follow/<path:id>', views.follow, name='follow'),
  path('inbox/', views.inbox, name='inbox'),

#--- below for the rest frame work ---#
  # path('', include(router.urls)),
  # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

  path('api/authors/', AuthorList.as_view(), name='authors_api'),
  path('api/authors/<str:id>/', SingleAuthor.as_view(), name='author_api'),
  path('api/authors/<str:id>/followers/', FollowerList.as_view(), name='followers_api'),
  path('api/authors/<str:id>/followers/<path:fid>/', singleFollowerList.as_view(), name='follower_api'),
  path('api/authors/<str:id>/posts/', PostsList.as_view(), name='posts_api'),
  path('api/authors/<str:id>/posts/<str:pid>/', SinglePost.as_view(), name='post_api'),
  path('api/authors/<str:id>/posts/<str:pid>/comments/', Commentlist.as_view(), name='comments_api'),
  # path('api/authors/<str:id>/followers',FollowerList.as_view(),name="followers_api"),
  # path('api/authors/<str:id>/followers/<str:fid>', singleFollowerList.as_view(),name="follower_api"),
  path('api/authors/<str:id>/posts/<str:pid>/image/', ImagePostsList.as_view(), name='image_api'),
  # path('api/authors/<str:id>/inbox/',inboxLikes.as_view(), name="inbox_likes"),
  path('api/authors/<str:id>/posts/<str:pid>/likes/',postLikes.as_view(), name="post_likes"),
  path('api/authors/<str:id>/posts/<str:pid>/comments/<str:cid>/likes/',commentLikes.as_view(), name="comment_likes"),
  path('api/authors/<str:id>/liked/', authorLikes.as_view(),name="liked"),
  path('api/authors/<str:id>/inbox/', InboxList.as_view(),name="Inbox"),


]