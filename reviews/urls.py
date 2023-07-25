from django.urls import path
from . import views

urlpatterns = [
    path("", views.Reviews.as_view()),
    path("/rooms", views.RoomReviews.as_view()),
    path("/rooms/<int:pk>", views.OneRoomAllReviews.as_view()),
    path("/experience", views.ExperienceReviews.as_view()),
    path("/experience/<int:pk>", views.OneExperienceAllReviews.as_view()),
    path("/<int:pk>", views.ReviewDetail.as_view()),
    path("/myReviews", views.MyReviews.as_view()),
]
