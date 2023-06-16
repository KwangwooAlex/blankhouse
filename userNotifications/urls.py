from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserNotifications_All.as_view()),
    path("/<int:pk>", views.UserNotification_Detail.as_view()),
]
