from django.urls import path
from . import views

urlpatterns = [
    path("", views.Chatrooms.as_view()),
    path("/create_room/<int:pk>", views.CreateChatrooms.as_view()),
    path("/<int:pk>", views.ChatroomsDetail.as_view()),
    path("/<int:pk>/directMessage", views.DirectMessage.as_view()),
]
