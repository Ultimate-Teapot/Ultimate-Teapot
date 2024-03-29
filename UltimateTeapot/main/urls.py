from django.urls import path
from . import views
from .views import AuthorList, SingleAuthor, PostsList, SinglePost, FollowerList, Commentlist, singleFollowerList, ImagePostsList, authorLikes,commentLikes,postLikes,InboxList


urlpatterns = [
  path('inbox/delete/', views.clear_inbox, name='clear_inbox'),
  path('', views.home, name='home'),
  path('teapot', views.teapot, name='teapot'),
  path('signup', views.signup, name='signup'),
  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
  path('like', views.like, name='like'),
  path('home/', views.home, name="home"),
  path('<str:post_id>/like/', views.like_create, name='like_create'),
  path('posts/<str:id>', views.post, name='post'),
  path('posts/', views.posts, name='posts'),
  path('posts/delete/<path:id>/', views.delete_post, name='delete_post'),
  path('posts/<path:id>/editpost/', views.edit_post, name='edit_post'),
  path('make_post/', views.make_post, name='make_post'),
  path('make_comment/<path:id>', views.make_comment, name='make_comment'),
  path('like_post/<path:id>', views.like_post, name='like_post'),
  path('like_comment/<path:id>', views.like_comment, name='like_comment'),
  path('foreign_post/<path:id>/', views.foreign_post, name='foreign_post'),
  path('authors/<str:author_id>/posts/<str:post_id>', views.singlePost, name='singlePost'),
  path('authors/<str:id>/posts/<str:post_id>/comment/', views.comment_create, name='comment_create'),
  path('authors/', views.authors, name='authors'),
  path('authors/<path:id>', views.profile, name='profile'),
  path('profile/<path:id>/edit_profile', views.edit_profile, name='edit_profile'),
  path('profile/<str:id>', views.user_profile, name='user_profile'),
  path('follow/<path:id>', views.follow, name='follow'),
  path('inbox/', views.inbox, name='inbox'),
  path('follow_response/', views.follow_response, name='follow_response'),
  path('send_unlisted_post/', views.send_unlisted_post, name='send_unlisted_post'),
  
#------- URLS for rest frame work -------#
  

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