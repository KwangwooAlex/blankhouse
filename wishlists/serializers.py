from rest_framework.serializers import ModelSerializer
from rooms.serializers import RoomListSerializer
from experiences.serializers import ExperienceListSerializer
from rest_framework import serializers

from .models import Wishlist


class RoomWishlistSerializer(ModelSerializer):
    rooms = RoomListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = ("rooms",)


class ExperienceWishlistSerializer(ModelSerializer):
    experiences = ExperienceListSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = ("experiences",)


class SaveRoomWishlistSerializer(ModelSerializer):
    room_pk = serializers.IntegerField()

    class Meta:
        model = Wishlist
        fields = ("room_pk",)


class SaveExperienceWishlistSerializer(ModelSerializer):
    experience_pk = serializers.IntegerField()

    class Meta:
        model = Wishlist
        fields = ("experience_pk",)
