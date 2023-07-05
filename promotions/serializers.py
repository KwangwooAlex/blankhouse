from rest_framework.serializers import ModelSerializer
from users.serializers import TinyUserSerializer, User_Id_Serializer
from .models import Promotion
from rest_framework import serializers


class PromotionSerializer(ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            "pk",
            "discount_rate",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
            # "",
            # "description",
        )


class PromotionDetailSerializer(ModelSerializer):
    users = TinyUserSerializer(many=True, read_only=True)  # read_only=True 없으면 미리 쿠폰못만듬

    # users = TinyUserSerializer(many=True, read_only=True)
    class Meta:
        model = Promotion
        fields = (
            "pk",
            "users",
            "name",
            "description",
            "discount_rate",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
            # "",
            # "description",
        )


class PromotionValideSerializer(ModelSerializer):
    # users_id = User_Id_Serializer(many=True)  # read_only=True 없으면 미리 쿠폰못만듬 이렇게 하니 객체의 어레이를 줘야함
    # users_id = serializers.IntegerField(many=True)  # read_only=True 없으면 미리 쿠폰못만듬
    users = serializers.ListField(child=serializers.IntegerField())

    # users = TinyUserSerializer(many=True, read_only=True)
    class Meta:
        model = Promotion
        fields = (
            "users",
            "name",
            "start_date",
            "end_date",
            "description",
            "discount_rate",
        )


class PromotionUsersSerializer(ModelSerializer):
    # users_id = User_Id_Serializer(many=True)  # read_only=True 없으면 미리 쿠폰못만듬 이렇게 하니 객체의 어레이를 줘야함
    # users_id = serializers.IntegerField(many=True)  # read_only=True 없으면 미리 쿠폰못만듬
    users = serializers.ListField(child=serializers.IntegerField())

    # users = TinyUserSerializer(many=True, read_only=True)
    class Meta:
        model = Promotion
        fields = ("users",)
