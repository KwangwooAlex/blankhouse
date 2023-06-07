from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Booking
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from . import serializers
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)


# Create your views here.
class BookingDetail(GenericAPIView):
    queryset = Booking.objects.all()  # 필수

    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        return serializers.BookingDetailSerializer

    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        booking = self.get_object(pk)
        serializer = serializers.BookingDetailSerializer(
            booking,
            context={"request": request},
            # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
            # context에 접근할수있음
        )
        return Response(serializer.data)

    # def put(self, request, pk):
    #     if request.user.is_superuser:
    #         booking = self.get_object(pk)
    #         serializer = serializers.PerkDetailSerializer(
    #             booking,
    #             data=request.data,
    #             partial=True,  # 부분적으로만 업데이트 허용!
    #         )
    #         # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
    #         if serializer.is_valid():
    #             updated_perk = serializer.save()
    #             return Response(
    #                 serializers.PerkDetailSerializer(updated_perk).data,
    #             )
    #         else:
    #             return Response(
    #                 serializer.errors,
    #                 status=HTTP_400_BAD_REQUEST,
    #          )

    def delete(self, request, pk):
        booking = self.get_object(pk)

        if request.user.is_superuser == False:
            if booking.user != request.user:
                raise PermissionDenied

        booking.delete()

        return Response(status=HTTP_204_NO_CONTENT)
