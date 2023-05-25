from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("/me", views.Me.as_view()),
    path("/me/password", views.UserPassword.as_view()),
    # 유저이름이 me가 될수있기애 유저 디테일을 볼려면 @를 붙여서 쓰자
    # path("@<str:username>", views.PublicUser.as_view()),
    # 다른방법으로 연습해봄.. 그냥 django내제된 유저 검증이 젤 편함
    path("/log-in", views.LogIn.as_view()),
    path("/log-out", views.LogOut.as_view()),
]
