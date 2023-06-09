from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.Categories.as_view()),
    path("/rooms", views.Room_Categories.as_view()),
    path("/experience", views.Experience_Categories.as_view()),
    path("/<int:pk>", views.CategoryDetail.as_view()),
    # path("/add", views.Categories.as_view()),
]
