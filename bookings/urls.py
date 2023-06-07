from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("/<int:pk>", views.BookingDetail.as_view()),
    # path("/add", views.Categories.as_view()),
]
