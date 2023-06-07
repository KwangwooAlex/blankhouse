from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("/perks", views.Perks.as_view()),
    path("/perks/<int:pk>", views.PerkDetail.as_view()),
    path("/<int:pk>/bookings", views.ExperienceBookings.as_view()),
    path("/<int:pk>/bookings/check", views.ExperienceBookingCheck.as_view()),
    # path("/rooms", views.Room_Categories.as_view()),
    # path("/experience", views.Experience_Categories.as_view()),
    # path("/add", views.Categories.as_view()),
]
