from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Photo
from rooms.serializers import TinyRoomSerializer
from experiences.serializers import TinyExperienceSerializer


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "picture",
            "description",
        )


class SaveUserAvatarSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = ("picture",)


class SaveRoomPhotoSerializer(ModelSerializer):
    room_pk = serializers.IntegerField(min_value=0)

    class Meta:
        model = Photo
        fields = (
            "picture",
            "description",
            "room_pk",
        )


class RealSaveRoomPhotoSerializer(ModelSerializer):
    room = TinyRoomSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = (
            "picture",
            "room",
        )


class SaveExperiencePhotoSerializer(ModelSerializer):
    experience_pk = serializers.IntegerField(min_value=0)

    class Meta:
        model = Photo
        fields = (
            "picture",
            "description",
            "experience_pk",
        )


class RealSaveExperiencePhotoSerializer(ModelSerializer):
    experience = TinyExperienceSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = (
            "picture",
            "experience",
        )
