from rest_framework import serializers
from users.serializers import TinyUserSerializer
from rooms.serializers import TinyRoomSerializer
from experiences.serializers import TinyExperienceSerializer

from .models import Review


class ReviewDetailSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    room = TinyRoomSerializer(read_only=True)
    experience = TinyExperienceSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "pk",
            "user",
            "room",
            "experience",
            "payload",
            "rating",
            "communication_rating",
            "location_rating",
            "accuracy_rating",
            "check_in_rating",
            "created_at",
            "updated_at",
        )


class ReviewSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    room = TinyRoomSerializer(read_only=True)
    experience = TinyExperienceSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "pk",
            "user",
            "room",
            "experience",
            # "payload",
            "created_at",
            "updated_at",
        )


class RoomReviewSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    room = TinyRoomSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "pk",
            "user",
            "room",
            # "payload",
            "rating",
            "communication_rating",
            "location_rating",
            "accuracy_rating",
            "check_in_rating",
            "created_at",
            "updated_at",
        )


class ExperienceReviewSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    experience = TinyExperienceSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "pk",
            "user",
            "experience",
            # "payload",
            "rating",
            "communication_rating",
            "location_rating",
            "accuracy_rating",
            "check_in_rating",
            "created_at",
            "updated_at",
        )


class RoomReviewSaveSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField()

    class Meta:
        model = Review
        fields = (
            "room_id",
            "payload",
            "rating",
            "communication_rating",
            "location_rating",
            "accuracy_rating",
            "check_in_rating",
            "created_at",
            "updated_at",
        )


class ExperienceReviewSaveSerializer(serializers.ModelSerializer):
    experience_id = serializers.IntegerField()

    class Meta:
        model = Review
        fields = (
            "experience_id",
            "payload",
            "rating",
            "communication_rating",
            "location_rating",
            "accuracy_rating",
            "check_in_rating",
        )


class ReviewEditSerializer(serializers.ModelSerializer):
    payload = serializers.CharField(required=False)
    rating = serializers.IntegerField(required=False, min_value=0, max_value=5)
    communication_rating = serializers.IntegerField(
        required=False, min_value=0, max_value=5
    )
    location_rating = serializers.IntegerField(required=False, min_value=0, max_value=5)
    accuracy_rating = serializers.IntegerField(required=False, min_value=0, max_value=5)
    check_in_rating = serializers.IntegerField(required=False, min_value=0, max_value=5)

    class Meta:
        model = Review
        fields = (
            "payload",
            "rating",
            "communication_rating",
            "location_rating",
            "accuracy_rating",
            "check_in_rating",
        )
