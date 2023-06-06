from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("/<int:pk>", views.RoomDetail.as_view()),
    path("/amenities", views.Amenities.as_view()),
    path("/amenities/<int:pk>", views.AmenityDetail.as_view()),
    path("/<int:pk>/bookings", views.RoomBookings.as_view()),
    path("/<int:pk>/bookings/check", views.RoomBookingCheck.as_view()),
    # path("/rooms", views.Room_Categories.as_view()),
    # path("/experience", views.Experience_Categories.as_view()),
    # path("/add", views.Categories.as_view()),
]
