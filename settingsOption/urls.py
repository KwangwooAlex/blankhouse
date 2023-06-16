from django.urls import path
from . import views

urlpatterns = [
    path("", views.SettingOption_All.as_view()),
    path("/<int:pk>", views.SettingOption_Detail.as_view()),
]
