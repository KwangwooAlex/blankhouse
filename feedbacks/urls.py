from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.Feedback_All.as_view()),
    path("/<int:pk>", views.FeedbackDetail.as_view()),
    path("/<int:pk>/answer", views.Create_Answer.as_view()),
    path("/answer/<int:pk>", views.AnswerDetail.as_view()),
]
