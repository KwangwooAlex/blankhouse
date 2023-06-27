from django.urls import path
from . import views

urlpatterns = [
    path("/room", views.RoomBookingHistories.as_view()),
    path("/experience", views.ExperienceBookingHistories.as_view()),
    path("/room/<int:pk>", views.RoomBookingDetailHistory.as_view()),
    path("/experience/<int:pk>", views.ExperienceBookingDetailHistory.as_view()),
    # path("orderHistory/<int:pk>", views.SoldProductDetail.as_view()),
]
