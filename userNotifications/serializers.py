from rest_framework.serializers import ModelSerializer
from users.serializers import TinyUserSerializer
from .models import UserNotifications
from rest_framework import serializers


class UserNotification_Detail(ModelSerializer):
    user = TinyUserSerializer()

    class Meta:
        model = UserNotifications
        fields = "__all__"


class UserNotifications_All(ModelSerializer):
    user = TinyUserSerializer()

    class Meta:
        model = UserNotifications
        fields = (
            "pk",
            "type",
            "name",
            "user",
            "is_read",
        )


class Create_UserNotification(ModelSerializer):
    user_id = serializers.IntegerField(min_value=1)

    class Meta:
        model = UserNotifications
        fields = (
            "type",
            "user_id",
            "name",
            "detail",
        )


class Edit_is_read_userNotification(ModelSerializer):
    class Meta:
        model = UserNotifications
        fields = ("is_read",)
