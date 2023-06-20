from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Chatroom

from direct_messages.models import DirectMessages
from direct_messages.serializers import PostDirectMessageSerializer

from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from . import serializers
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from django.db import transaction
from users.models import User
from rest_framework.generics import GenericAPIView


class Chatrooms(GenericAPIView):
    queryset = Chatroom.objects.all()  # 필수
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return serializers.ChatroomSerializer
        return serializers.ChatroomSerializer

    def get(self, request):
        if request:
            print("requestrequest", request.user)
            all_chatrooms = Chatroom.objects.filter(user=request.user)
            serializer = serializers.ChatroomSerializer(
                all_chatrooms,
                many=True,
                context={"request": request},
                # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
                # context에 접근할수있음
            )
            return Response(serializer.data)
        return False


class CreateChatrooms(GenericAPIView):
    queryset = Chatroom.objects.all()  # 필수
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.CreateChatroomSerializer

    def post(self, request, pk):
        serializer = serializers.CreateChatroomSerializer(data=request.data)
        # try:
        #     with transaction.atomic():
        if serializer.is_valid():
            another_user = User.objects.filter(pk=pk)[0]
            if another_user:
                if (
                    Chatroom.objects.filter(user=request.user)
                    .filter(user=another_user)
                    .exists()
                ):
                    raise ParseError("This user already has a chat room with the user")

                chatroom = serializer.save(user=[request.user, another_user])
                serializer = serializers.ChatroomSerializer(
                    chatroom,
                    context={"request": request},
                )
                serializer.save
                return Response(serializer.data)
            else:
                raise ParseError("User not found")
        # except Exception:
        #     raise ParseError(
        #         "user not found by user try or already has a room check backend and search!!"
        #     )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class ChatroomsDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, request, pk):
        # if request.user.is_superuser:
        #     try:
        #         return Chatroom.objects.filter(pk=pk)
        #     except Chatroom.DoesNotExist:
        #         raise NotFound
        # else:
        try:
            return Chatroom.objects.filter(user=request.user, pk=pk)
        except Chatroom.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        if self.get_object(request, pk).exists():
            Chatroom = self.get_object(request, pk)
            serializer = serializers.ChatroomDetailSerializer(
                Chatroom,
                many=True,
                context={"request": request},
            )
            return Response(serializer.data)
        else:
            raise ParseError("You can not see this room")

    def delete(self, request, pk):
        if self.get_object(request, pk).exists():
            chatroom = self.get_object(request, pk)
            chatroom.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            raise ParseError("You can not remove this room")


class DirectMessage(GenericAPIView):
    queryset = DirectMessages.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return PostDirectMessageSerializer

    def post(self, request, pk):
        serializer = PostDirectMessageSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():  # transaction 써줘야 만들다가 실패하면 rollback함
                    # 일반유저가 방을만들면 자기자신이름으로 방을 만든다!

                    if (
                        Chatroom.objects.filter(pk=pk)
                        .filter(user=request.user)
                        .exists()
                    ):
                        chatroom = Chatroom.objects.filter(pk=pk).filter(
                            user=request.user
                        )[0]

                        directMessage = serializer.save(
                            chatroom=chatroom,
                            user=request.user,
                            payload=request.data.get("payload"),
                        )

                        serializer = serializers.DirectMessageSerializer(
                            directMessage,
                            context={"request": request},
                        )

                        return Response(serializer.data)
                    else:
                        raise ParseError("error")

            except Exception:
                # transaction 이 실패하면 에러를 낼것임
                raise ParseError(
                    "Room does not exist or you can not send message to this room"
                )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )
