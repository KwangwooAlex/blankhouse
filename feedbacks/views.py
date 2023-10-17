from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from . import serializers
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from .models import Feedback, Answer
from rest_framework.generics import GenericAPIView


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "kind",
                openapi.IN_QUERY,
                description="filter by kind",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class Feedback_All(GenericAPIView):
    queryset = Feedback.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        return serializers.Save_Feedback_Serializer

    def get_object(self):
        try:
            return Feedback.objects.all()
        except Feedback.DoesNotExist:
            raise NotFound

    def get(self, request):
        Feedback = self.get_object()
        Feedback = (
            Feedback.filter(kind=request.query_params.get("kind"))
            if request.query_params.get("kind")
            else Feedback
        )

        serializer = serializers.FeedbackList_Serializer(
            Feedback,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        # web에서 받아온 데이터를 json으로 번역해서 django에 넘겨야함
        # 그다음 필요한내용을 하고 결과내용을 다시 json으로 번역해서 web에 넘겨야함
        serializer = serializers.Save_Feedback_Serializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save(
                writer=request.user,
                status="pending",
            )
            serializer = serializers.Feedback_Detail_Serializer(
                feedback,
                context={"request": request},
            )
            return Response(serializer.data)

        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class FeedbackDetail(GenericAPIView):
    queryset = Feedback.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.Save_Feedback_Serializer
        if self.request.method == "PUT":
            return serializers.Edit_Feedback_Serializer
        return serializers.Save_Feedback_Serializer

    def get_object(self, pk):
        try:
            return Feedback.objects.get(pk=pk)
        except Feedback.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # if request.user.is_superuser:
        # 전체 방리뷰만 보여주세요 리뷰에 room없으면 제외 해주세요
        # 모든사람이 다 리뷰를 볼수있음!
        feedback = self.get_object(pk)
        serializer = serializers.Feedback_Detail_Serializer(
            feedback,
            context={"request": request},
            # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
            # context에 접근할수있음
        )
        return Response(serializer.data)

    def put(self, request, pk):
        feedback = self.get_object(pk)
        serializer = serializers.Edit_Feedback_Serializer(
            feedback,
            data=request.data,
            partial=True,  # 부분적으로만 업데이트 허용!
        )
        # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
        if serializer.is_valid():
            updated_feedback = serializer.save()
            return Response(
                serializers.Feedback_Detail_Serializer(updated_feedback).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        feedback = self.get_object(pk)
        if request.user.is_superuser == False:
            if feedback.user != request.user:
                raise PermissionDenied

        feedback.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Create_Answer(GenericAPIView):
    queryset = Answer.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.RoomReviewSaveSerializer
        return serializers.Save_Answer_Serializer

    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # if request.user.is_superuser:
        # 전체 방리뷰만 보여주세요 리뷰에 room없으면 제외 해주세요
        # 모든사람이 다 리뷰를 볼수있음!
        all_reviews = Answer.objects.filter(feedback_id=pk)
        serializer = serializers.Save_Answer_Serializer(
            all_reviews,
            many=True,
            context={"request": request},
            # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
            # context에 접근할수있음
        )
        return Response(serializer.data)


class AnswerDetail(GenericAPIView):
    queryset = Answer.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.RoomReviewSaveSerializer
        if self.request.method == "PUT":
            return serializers.Edit_Answer_Serializer
        return serializers.Save_Answer_Serializer

    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        Answer = self.get_object(pk)
        serializer = serializers.Edit_Answer_Serializer(
            Answer,
            data=request.data,
            partial=True,  # 부분적으로만 업데이트 허용!
        )
        # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
        if serializer.is_valid():
            updated_answer = serializer.save()
            return Response(
                serializers.Detail_Answer_Serializer(updated_answer).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        answer = self.get_object(pk)
        if request.user.is_superuser == False:
            if answer.user != request.user:
                raise PermissionDenied

        answer.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    # else:
    #     user_reviews = Review.objects.filter(user=request.user)
    #     all_user_room_reviews = user_reviews.exclude(room__isnull=True)
    #     serializer = serializers.RoomReviewSerializer(
    #         all_user_room_reviews,
    #         many=True,
    #         context={"request": request},
    #         # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
    #         # context에 접근할수있음
    #     )
    #     return Response(serializer.data)

    # def post(self, request):
    #     # web에서 받아온 데이터를 json으로 번역해서 django에 넘겨야함
    #     # 그다음 필요한내용을 하고 결과내용을 다시 json으로 번역해서 web에 넘겨야함
    #     serializer = serializers.RoomReviewSaveSerializer(data=request.data)
    #     if serializer.is_valid():
    #         room = Room.objects.get(pk=request.data.get("room_id"))

    #         review = serializer.save(
    #             user=request.user,
    #             room=room,
    #         )

    #         serializer = serializers.ReviewDetailSerializer(
    #             review,
    #             context={"request": request},
    #         )

    #         return Response(serializer.data)

    #     else:
    #         return Response(
    #             serializer.errors,
    #             status=HTTP_400_BAD_REQUEST,
    #         )
