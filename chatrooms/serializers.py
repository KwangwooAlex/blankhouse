from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.serializers import TinyUserSerializer
from .models import Chatroom
from direct_messages.serializers import DirectMessageSerializer


class ChatroomPostSerializer(ModelSerializer):
    class Meta:
        model = Chatroom
        fields = (
            "pk",
            "created_at",
            "updated_at",
        )


class ChatroomSerializer(ModelSerializer):
    user = TinyUserSerializer(many=True, read_only=True)

    class Meta:
        model = Chatroom
        fields = (
            "pk",
            "user",
            "created_at",
            "updated_at",
        )


class CreateChatroomSerializer(ModelSerializer):
    # directMessage = DirectMessageSerializer(many=True, read_only=True)
    user_id = serializers.ReadOnlyField()

    class Meta:
        model = Chatroom
        fields = (
            "pk",
            "user_id",
            "created_at",
            "updated_at",
        )


class ChatroomDetailSerializer(ModelSerializer):
    user = TinyUserSerializer(many=True, read_only=True)
    directMessage = DirectMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chatroom
        fields = (
            "pk",
            "user",
            "directMessage",
            "created_at",
            "updated_at",
        )
