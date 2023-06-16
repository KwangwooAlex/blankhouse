from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import UserNotifications
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
from users.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)


class UserNotification_Detail(GenericAPIView):
    queryset = UserNotifications.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.Edit_is_read_userNotification
        return serializers.UserNotification_Detail

    def get_object(self, request, pk):
        try:
            return UserNotifications.objects.get(pk=pk, user=request.user)
        except UserNotifications.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        # request_body=serializers.EditAmenitySerializer,
        # tags=["Amenities"],
        # operation_id="This is testing api ID 111",
        operation_summary="Will return only notifications the correct user has",
        # operation_description="Modify Amenity detail",
        # deprecated=True,
    )
    def get(self, request, pk):
        UserNotifications = self.get_object(request, pk)
        serializer = serializers.UserNotification_Detail(
            UserNotifications,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        notification = self.get_object(request, pk)
        print("notification11111", notification.user)
        print("notification22222", request.user)

        if notification.user == request.user:
            serializer = serializers.Edit_is_read_userNotification(
                notification,
                data=request.data,
                partial=True,  # 부분적으로만 업데이트 허용!
            )
            # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
            if serializer.is_valid():
                updated_notification = serializer.save()
                return Response(
                    serializers.UserNotification_Detail(updated_notification).data,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )
        else:
            raise PermissionDenied

    def delete(self, request, pk):
        notification = self.get_object(request, pk)
        if notification.user == request.user:
            notification.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_401_UNAUTHORIZED)


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
        ],
        operation_summary="Will return only notifications the correct user has",
    ),
)
class UserNotifications_All(GenericAPIView):
    queryset = UserNotifications.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.Create_UserNotification
        return serializers.UserNotifications_All

    def get_object(self, request):
        try:
            return UserNotifications.objects.filter(user=request.user)
        except UserNotifications.DoesNotExist:
            raise NotFound

    def get(self, request):
        UserNotifications = self.get_object(request)

        UserNotifications = (
            UserNotifications.filter(type=request.query_params.get("type"))
            if request.query_params.get("type")
            else UserNotifications
        )

        serializer = serializers.UserNotifications_All(
            UserNotifications,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.Create_UserNotification(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            user = User.objects.filter(pk=request.data.get("user_id"))[0]

            notification = serializer.save(
                user=user,
            )
            serializer = serializers.UserNotification_Detail(notification)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )
