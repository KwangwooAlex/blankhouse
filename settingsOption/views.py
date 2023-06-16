from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import SettingsOption
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from . import serializers
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema


class SettingOption_Detail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        return serializers.SettingOption_Detail

    def get_object(self, pk):
        try:
            return SettingsOption.objects.get(pk=pk)
        except SettingsOption.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        SettingsOption = self.get_object(pk)
        serializer = serializers.SettingOption_Detail(
            SettingsOption,
            context={"request": request},
        )
        return Response(serializer.data)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "type",
                openapi.IN_QUERY,
                description="filter by type",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class SettingOption_All(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        return serializers.SettingOption_All

    def get_object(self):
        try:
            return SettingsOption.objects.all()
        except SettingsOption.DoesNotExist:
            raise NotFound

    def get(self, request):
        SettingsOption = self.get_object()

        SettingsOption = (
            SettingsOption.filter(type=request.query_params.get("type"))
            if request.query_params.get("type")
            else SettingsOption
        )

        serializer = serializers.SettingOption_All(
            SettingsOption,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)
