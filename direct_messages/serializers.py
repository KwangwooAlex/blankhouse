from rest_framework import serializers
from users.serializers import TinyUserSerializer

from .models import DirectMessages


class PostDirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessages
        fields = (
            "payload",
            "created_at",
            "updated_at",
        )


class DirectMessageSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = DirectMessages
        fields = (
            "user",
            "chatroom",
            "payload",
            "created_at",
            "updated_at",
        )
