from rest_framework.serializers import ModelSerializer
from .models import Category


class AddCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "pk",
            "name",
            "kind",
        )


class EditCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)
