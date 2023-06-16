from rest_framework.serializers import ModelSerializer
from users.serializers import TinyUserSerializer
from .models import SettingsOption


class SettingOption_Detail(ModelSerializer):
    class Meta:
        model = SettingsOption
        fields = "__all__"


class SettingOption_All(ModelSerializer):
    class Meta:
        model = SettingsOption
        fields = (
            "pk",
            "type",
            "name",
        )
