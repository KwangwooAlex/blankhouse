from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User
from photos.serializers import SaveUserAvatarSerializer


class PrivateUserSerializer(ModelSerializer):
    avatar = SaveUserAvatarSerializer(read_only=True)

    class Meta:
        model = User
        # exclude 임!!!!!!!

        exclude = (
            "groups",
            "user_permissions",
            "password",
            "last_login",
            "is_active",
            "date_joined",
        )


class EditUserSerializer(ModelSerializer):
    username = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "balance",
            "address",
            "emergency_contact",
            "phone_number",
            "is_host",
            "born_year",
            "school",
            "work",
            "hobby",
            "gender",
            "language",
            "currency",
        )


class EditPWUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("password",)


class AllUserSerializer(ModelSerializer):
    avatar = SaveUserAvatarSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "pk",
            "avatar",
            "username",
            "email",
            "phone_number",
            "gender",
            "is_host",
            "is_superuser",
            "is_staff",
        )


# old one


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "name",
            "username",
        )


class User_Id_Serializer(ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ("user_id",)


class PkUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("pk",)


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "name",
            "username",
        )


class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "password",
        )
