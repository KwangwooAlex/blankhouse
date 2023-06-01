from django.urls import path
from . import views

urlpatterns = [
    path("/<int:pk>", views.PhotoDetail.as_view()),
    path("/user/avatar", views.UserAvatar.as_view()),
    path("/room/picture", views.PhotoToRoom.as_view()),
    path("/experience/picture", views.PhotoToExperience.as_view()),
]
