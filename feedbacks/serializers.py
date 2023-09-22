from rest_framework import serializers
from users.serializers import TinyUserSerializer

from .models import Feedback


class FeedbackList_Serializer(serializers.ModelSerializer):
    writer = TinyUserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = (
            "pk",
            "writer",
            "kind",
            "status",
            "created_at",
            "updated_at",
        )


class Feedback_Detail_Serializer(serializers.ModelSerializer):
    writer = TinyUserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = (
            "pk",
            "writer",
            "kind",
            "details",
            "status",
            "created_at",
            "updated_at",
        )


class Edit_Feedback_Serializer(serializers.ModelSerializer):
    details = serializers.CharField(required=False)

    class Meta:
        model = Feedback
        fields = (
            "status",
            "details",
        )


class Save_Feedback_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = (
            "kind",
            "details",
            "created_at",
            "updated_at",
        )
