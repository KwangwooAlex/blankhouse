from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from . import serializers
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.generics import GenericAPIView
from django.db import transaction

# Create your views here.


class Categories(GenericAPIView):
    queryset = Category.objects.all()  # 필수
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        return serializers.AddCategorySerializer

    def get(self, request):
        all_room_categories = Category.objects.all()
        serializer = serializers.AddCategorySerializer(
            all_room_categories,
            many=True,
            context={"request": request},
            # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
            # context에 접근할수있음
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.AddCategorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():  # transaction 써줘야 만들다가 실패하면 rollback함
                    newCategory = serializer.save()
                    serializer = serializers.AddCategorySerializer(
                        newCategory,
                        context={"request": request},
                    )

                return Response(serializer.data)
            except Exception:
                # transaction 이 실패하면 에러를 낼것임
                raise ParseError(
                    "product not found, check backend cart view and search!!"
                )

        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class Room_Categories(GenericAPIView):
    queryset = Category.objects.all()  # 필수
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        return serializers.AddCategorySerializer

    def get(self, request):
        all_room_categories = Category.objects.filter(kind="rooms")
        serializer = serializers.AddCategorySerializer(
            all_room_categories,
            many=True,
            context={"request": request},
            # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
            # context에 접근할수있음
        )
        return Response(serializer.data)


class Experience_Categories(GenericAPIView):
    queryset = Category.objects.all()  # 필수
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        return serializers.AddCategorySerializer

    def get(self, request):
        all_experiences_categories = Category.objects.filter(kind="experiences")
        serializer = serializers.AddCategorySerializer(
            all_experiences_categories,
            many=True,
            context={"request": request},
            # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
            # context에 접근할수있음
        )
        return Response(serializer.data)


class CategoryDetail(GenericAPIView):
    queryset = Category.objects.all()  # 필수

    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.EditCategorySerializer

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        if request.user.is_superuser:
            category = self.get_object(pk)
            serializer = serializers.EditCategorySerializer(
                category,
                data=request.data,
                partial=True,  # 부분적으로만 업데이트 허용!
            )
            # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
            if serializer.is_valid():
                updated_category = serializer.save()
                return Response(
                    serializers.AddCategorySerializer(updated_category).data,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )

    def delete(self, request, pk):
        category = self.get_object(pk)

        if request.user.is_superuser == False:
            raise PermissionDenied

        category.delete()

        return Response(status=HTTP_204_NO_CONTENT)
