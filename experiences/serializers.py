from rest_framework.serializers import ModelSerializer
from .models import Perk


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = (
            "pk",
            "name",
            "details",
        )


class PerkDetailSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = (
            "pk",
            "name",
            "details",
            "explanation",
        )


class EditPerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = (
            "name",
            "details",
        )
