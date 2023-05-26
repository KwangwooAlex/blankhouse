from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("/rooms", views.RoomWishlists.as_view()),
    path("/experiences", views.ExperienceWishlists.as_view()),
]
