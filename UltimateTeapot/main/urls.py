from django.urls import path,include
from . import views
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
  path('home/', views.home, name="home"),
  #path('', views.index, name='index'),
  path('posts/', views.posts, name='posts'),
  path('authors/', views.authors, name='authors'),
  path('authors/<str:username>', views.profile, name='profile'),

  #--- below for the rest frame work ---#
  # path('', include(router.urls)),
  # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]