from django.urls import path
from . import views

urlpatterns = [
    path("", views.Reviews.as_view()),
    path("/rooms", views.RoomReviews.as_view()),
    path("/experience", views.ExperienceReviews.as_view()),
    path("/<int:pk>", views.ReviewDetail.as_view()),
]
