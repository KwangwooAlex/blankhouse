from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Promotion
from users.models import User
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
from django.db import transaction
from rest_framework.generics import GenericAPIView


class Promotions(GenericAPIView):
    queryset = Promotion.objects.all()  # 필수
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.PromotionValideSerializer
        return serializers.PromotionSerializer

    def get(self, request):
        if request.user.is_superuser:
            all_promotions = Promotion.objects.all()
            serializer = serializers.PromotionSerializer(
                all_promotions,
                many=True,
                context={"request": request},
                # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
                # context에 접근할수있음
            )
            return Response(serializer.data)
        else:
            user_promotions = Promotion.objects.filter(users=request.user)
            serializer = serializers.PromotionSerializer(
                user_promotions,
                many=True,
                context={"request": request},
                # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
                # context에 접근할수있음
            )
        return Response(serializer.data)

    def post(self, request):
        # web에서 받아온 데이터를 json으로 번역해서 django에 넘겨야함
        # 그다음 필요한내용을 하고 결과내용을 다시 json으로 번역해서 web에 넘겨야함
        serializer = serializers.PromotionValideSerializer(data=request.data)
        error = ""
        if serializer.is_valid():
            try:
                with transaction.atomic():  # transaction 써줘야 만들다가 실패하면 rollback함
                    # 1 쿼리
                    coupon = serializer.save()

                    users = request.data.get("users")
                    print("users", users)
                    # 2쿼리
                    for user_pk in users:
                        user = User.objects.get(pk=user_pk)
                        coupon.users.add(user)

                    serializer = serializers.PromotionDetailSerializer(
                        coupon,
                        context={"request": request},
                    )

                    return Response(serializer.data)
            except Exception:
                # transaction 이 실패하면 에러를 낼것임
                raise ParseError("user not found or wrong discount number")

        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class PromotionDetail(GenericAPIView):
    queryset = Promotion.objects.all()  # 필수
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.PromotionDetailSerializer
        return serializers.PromotionDetailSerializer

    def get_object(self, pk):
        try:
            return Promotion.objects.get(pk=pk)
        except Promotion.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        Promotion = self.get_object(pk)
        serializer = serializers.PromotionDetailSerializer(
            Promotion,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.is_superuser:
            Promotion = self.get_object(pk)
            serializer = serializers.PromotionDetailSerializer(
                Promotion,
                data=request.data,
                partial=True,  # 부분적으로만 업데이트 허용!
            )
            # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
            if serializer.is_valid():
                updated_promotion = serializer.save()
                return Response(
                    serializers.PromotionDetailSerializer(updated_promotion).data,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )
        return Response(status=HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        promotion = self.get_object(pk)
        promotion.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class PromotionUserAddControl(GenericAPIView):
    queryset = Promotion.objects.all()  # 필수
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.PromotionUsersSerializer

    def get_object(self, pk):
        try:
            return Promotion.objects.get(pk=pk)
        except Promotion.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        if request.user.is_superuser:
            Promotion = self.get_object(pk)
            serializer = serializers.PromotionDetailSerializer(
                Promotion,
                data=request.data,
                partial=True,  # 부분적으로만 업데이트 허용!
            )
            # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
            if serializer.is_valid():
                updated_promotion = serializer.save()
                users = request.data.get("users")
                for user_pk in users:
                    user = User.objects.get(pk=user_pk)
                    updated_promotion.users.add(user)

                return Response(
                    serializers.PromotionDetailSerializer(updated_promotion).data,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )
        return Response(status=HTTP_401_UNAUTHORIZED)


class PromotionUserRemoveControl(GenericAPIView):
    queryset = Promotion.objects.all()  # 필수
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.PromotionUsersSerializer

    def get_object(self, pk):
        try:
            return Promotion.objects.get(pk=pk)
        except Promotion.DoesNotExist:
            raise NotFound

    def put(self, request, pk):
        if request.user.is_superuser:
            Promotion = self.get_object(pk)
            serializer = serializers.PromotionDetailSerializer(
                Promotion,
                data=request.data,
                partial=True,  # 부분적으로만 업데이트 허용!
            )
            # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
            if serializer.is_valid():
                updated_promotion = serializer.save()
                users = request.data.get("users")
                for user_pk in users:
                    user = User.objects.get(pk=user_pk)
                    updated_promotion.users.remove(user)

                return Response(
                    serializers.PromotionDetailSerializer(updated_promotion).data,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )
        return Response(status=HTTP_401_UNAUTHORIZED)
