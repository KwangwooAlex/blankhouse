from rest_framework import serializers
from users.serializers import TinyUserSerializer

from .models import Feedback, Answer


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


class Detail_For_Feedback_Answer_Serializer(serializers.ModelSerializer):
    writer = TinyUserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = (
            "pk",
            "writer",
            "details",
            "created_at",
            "updated_at",
        )


class Feedback_Detail_Serializer(serializers.ModelSerializer):
    writer = TinyUserSerializer(read_only=True)
    answers = Detail_For_Feedback_Answer_Serializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = (
            "pk",
            "writer",
            "kind",
            "details",
            "answers",
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


class Save_Answer_Serializer(serializers.ModelSerializer):
    feedback = Feedback_Detail_Serializer(read_only=True)
    writer = TinyUserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = (
            "pk",
            "writer",
            "feedback",
            "details",
            "created_at",
            "updated_at",
        )


class Edit_Answer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("details",)


class Detail_Answer_Serializer(serializers.ModelSerializer):
    feedback = Feedback_Detail_Serializer(read_only=True)
    writer = TinyUserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = (
            "pk",
            "writer",
            "feedback",
            "details",
            "created_at",
            "updated_at",
        )
