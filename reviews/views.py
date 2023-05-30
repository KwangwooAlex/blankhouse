import requests
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Review
from . import serializers
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.generics import GenericAPIView
from rooms.models import Room
from experiences.models import Experience


class Reviews(GenericAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        return serializers.ReviewSerializer

    def get_object(self, pk):
        try:
            # print("asdfasdfasfd", pk)
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise NotFound

    def get(self, request):
        if request.user.is_superuser:
            all_reviews = Review.objects.all()
            serializer = serializers.ReviewSerializer(
                all_reviews,
                many=True,
                context={"request": request},
                # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
                # context에 접근할수있음
            )
            return Response(serializer.data)
        else:
            user_reviews = Review.objects.filter(user=request.user)
            serializer = serializers.ReviewSerializer(
                user_reviews,
                many=True,
                context={"request": request},
                # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
                # context에 접근할수있음
            )
            return Response(serializer.data)


class RoomReviews(GenericAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.RoomReviewSaveSerializer
        return serializers.RoomReviewSerializer

    def get_object(self, pk):
        try:
            # print("asdfasdfasfd", pk)
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise NotFound

    def get(self, request):
        if request.user.is_superuser:
            all_reviews = Review.objects.exclude(room__isnull=True)
            serializer = serializers.RoomReviewSerializer(
                all_reviews,
                many=True,
                context={"request": request},
                # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
                # context에 접근할수있음
            )
            return Response(serializer.data)
        else:
            user_reviews = Review.objects.filter(user=request.user)
            all_user_room_reviews = user_reviews.exclude(room__isnull=True)
            serializer = serializers.RoomReviewSerializer(
                all_user_room_reviews,
                many=True,
                context={"request": request},
                # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
                # context에 접근할수있음
            )
            return Response(serializer.data)

    def post(self, request):
        # web에서 받아온 데이터를 json으로 번역해서 django에 넘겨야함
        # 그다음 필요한내용을 하고 결과내용을 다시 json으로 번역해서 web에 넘겨야함
        serializer = serializers.RoomReviewSaveSerializer(data=request.data)
        if serializer.is_valid():
            room = Room.objects.get(pk=request.data.get("room_id"))

            review = serializer.save(
                user=request.user,
                room=room,
            )

            serializer = serializers.ReviewDetailSerializer(
                review,
                context={"request": request},
            )

            return Response(serializer.data)

        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class ExperienceReviews(GenericAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.ExperienceReviewSaveSerializer
        return serializers.ExperienceReviewSerializer

    def get_object(self, pk):
        try:
            # print("asdfasdfasfd", pk)
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise NotFound

    def get(self, request):
        if request.user.is_superuser:
            all_reviews = Review.objects.exclude(experience__isnull=True)
            serializer = serializers.ExperienceReviewSerializer(
                all_reviews,
                many=True,
                context={"request": request},
                # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
                # context에 접근할수있음
            )
            return Response(serializer.data)
        else:
            user_reviews = Review.objects.filter(user=request.user)
            all_user_experience_reviews = user_reviews.exclude(experience__isnull=True)
            serializer = serializers.ExperienceReviewSerializer(
                all_user_experience_reviews,
                many=True,
                context={"request": request},
                # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
                # context에 접근할수있음
            )
            return Response(serializer.data)

    def post(self, request):
        # web에서 받아온 데이터를 json으로 번역해서 django에 넘겨야함
        # 그다음 필요한내용을 하고 결과내용을 다시 json으로 번역해서 web에 넘겨야함
        serializer = serializers.ExperienceReviewSaveSerializer(data=request.data)
        if serializer.is_valid():
            experience = Experience.objects.get(pk=request.data.get("experience_id"))

            review = serializer.save(
                user=request.user,
                experience=experience,
            )

            serializer = serializers.ReviewDetailSerializer(
                review,
                context={"request": request},
            )

            return Response(serializer.data)

        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class ReviewDetail(GenericAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.ReviewEditSerializer
        return serializers.ReviewDetailSerializer

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = serializers.ReviewDetailSerializer(
            review,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        review = self.get_object(pk)
        serializer = serializers.ReviewEditSerializer(
            review,
            data=request.data,
            partial=True,  # 부분적으로만 업데이트 허용!
        )
        # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
        if serializer.is_valid():
            updated_review = serializer.save()
            return Response(
                serializers.ReviewDetailSerializer(updated_review).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        review = self.get_object(pk)

        if request.user.is_superuser == False:
            if review.user != request.user:
                raise PermissionDenied

        review.delete()

        return Response(status=HTTP_204_NO_CONTENT)
