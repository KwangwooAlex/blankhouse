from django.urls import path
from . import views

urlpatterns = [
    path("", views.Promotions.as_view()),
    path("<int:pk>", views.PromotionDetail.as_view()),
    path("<int:pk>/addUsers", views.PromotionUserAddControl.as_view()),
    path("<int:pk>/removeUsers", views.PromotionUserRemoveControl.as_view()),
]
