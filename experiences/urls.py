from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.Experiences.as_view()),
    path("/<int:pk>", views.ExperienceDetail.as_view()),
    path("/perks", views.Perks.as_view()),
    path("/perks/<int:pk>", views.PerkDetail.as_view()),
    path("/<int:pk>/bookings", views.ExperienceBookings.as_view()),
    path("/<int:pk>/bookings/check", views.ExperienceBookingCheck.as_view()),
    # path("/rooms", views.Room_Categories.as_view()),
    # path("/experience", views.Experience_Categories.as_view()),
    # path("/add", views.Categories.as_view()),
]


# {
#     "name": "testing ex",
#     "country": "canada",
#     "city": "calgary",
#     "price": 5,
#     "address": "address is here",
#     "start": "12:45",
#     "end": "19:52",
#     "things_to_know": "its nice to know",
#     "perks_id": [1, 2, 3],
#     "category_id": 2,
#     "description": "hello",
#     "total_available_guest": 3,
# }
