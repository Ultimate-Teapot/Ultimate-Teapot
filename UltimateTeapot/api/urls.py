from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users',views.UserViewSet)
router.register(r'authors', views.ProfileViewSet)
router.register(r'posts', views.PostViewSet)



urlpatterns = [
  #--- below for the rest frame work ---#
  path('', include(router.urls)),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]