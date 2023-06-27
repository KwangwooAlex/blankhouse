from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import BookingHistory
from users.models import User
from bookings.models import Booking
from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from . import serializers

from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.generics import GenericAPIView
from django.db import transaction


class RoomBookingHistories(GenericAPIView):
    queryset = BookingHistory.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.CreateBookingHistorSerializer
        return serializers.RoomBookingHistorySerializer

    def get(self, request):
        if request:
            all_bookingHistory = BookingHistory.objects.filter(
                booking__user=request.user, booking__kind="room"
            )
            serializer = serializers.RoomBookingHistorySerializer(
                all_bookingHistory,
                many=True,
                context={"request": request},
                # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
                # context에 접근할수있음
            )
            return Response(serializer.data)
        return False

    def post(self, request):
        serializer = serializers.CreateBookingHistorSerializer(
            data=request.data,
        )
        error = ""
        try:
            with transaction.atomic():
                if serializer.is_valid():
                    booking = Booking.objects.filter(pk=request.data.get("booking_id"))[
                        0
                    ]
                    bookingHistory = serializer.save(booking=booking)
                    user = User.objects.get(username=request.user.username)
                    # if user.balance - order.total_price() < 0:
                    if (user.balance - bookingHistory.final_total_cost) < 0:
                        error = "Your balance is not enough."
                        print("errorerror", error)
                        raise ParseError("Your balance is not enough.")
                    user.balance = request.user.balance - request.data.get(
                        "final_total_cost"
                    )
                    user.save()

                    serializer = serializers.HistorDetailSerializer(bookingHistory)
                    return Response(serializer.data)
                else:
                    return Response(
                        serializer.errors,
                        status=HTTP_400_BAD_REQUEST,
                    )
        except Exception:
            # transaction 이 실패하면 에러를 낼것임
            raise ParseError(error)


class RoomBookingDetailHistory(GenericAPIView):
    queryset = BookingHistory.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        # if self.request.method == "POST":
        #     return serializers.OrderSaveForDocSerializer
        return serializers.HistorDetailSerializer

    def get_object(self, request, pk):
        try:
            return BookingHistory.objects.filter(
                booking__user=request.user, pk=pk
            ).first()
        except BookingHistory.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        BookingHistory = self.get_object(request, pk)
        serializer = serializers.HistorDetailSerializer(
            BookingHistory,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        bookingHistory = self.get_object(request, pk)
        print("bookingHistorybookingHistory", bookingHistory)
        if bookingHistory == None:
            raise PermissionDenied
        if request.user.is_superuser == False:
            if bookingHistory.booking.user != request.user:
                raise PermissionDenied

        bookingHistory.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class ExperienceBookingHistories(GenericAPIView):
    queryset = BookingHistory.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.CreateExperienceBookingHistorSerializer
        return serializers.ExperienceBookingHistorySerializer

    def get(self, request):
        if request:
            all_bookingHistory = BookingHistory.objects.filter(
                booking__user=request.user, booking__kind="experience"
            )
            serializer = serializers.ExperienceBookingHistorySerializer(
                all_bookingHistory,
                many=True,
                context={"request": request},
                # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
                # context에 접근할수있음
            )
            return Response(serializer.data)
        return False

    def post(self, request):
        serializer = serializers.CreateExperienceBookingHistorSerializer(
            data=request.data,
        )
        error = ""
        try:
            with transaction.atomic():
                if serializer.is_valid():
                    booking = Booking.objects.filter(pk=request.data.get("booking_id"))[
                        0
                    ]
                    bookingHistory = serializer.save(booking=booking)
                    user = User.objects.get(username=request.user.username)
                    # if user.balance - order.total_price() < 0:
                    if (user.balance - bookingHistory.final_total_cost) < 0:
                        error = "Your balance is not enough."
                        raise ParseError("Your balance is not enough.")
                    user.balance = request.user.balance - request.data.get(
                        "final_total_cost"
                    )
                    user.save()

                    serializer = serializers.ExperienceHistorDetailSerializer(
                        bookingHistory
                    )
                    return Response(serializer.data)
                else:
                    return Response(
                        serializer.errors,
                        status=HTTP_400_BAD_REQUEST,
                    )
        except Exception:
            # transaction 이 실패하면 에러를 낼것임
            raise ParseError(error)


class ExperienceBookingDetailHistory(GenericAPIView):
    queryset = BookingHistory.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        # if self.request.method == "POST":
        #     return serializers.OrderSaveForDocSerializer
        return serializers.HistorDetailSerializer

    def get_object(self, request, pk):
        try:
            return BookingHistory.objects.filter(
                booking__user=request.user, pk=pk
            ).first()
        except BookingHistory.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        BookingHistory = self.get_object(request, pk)
        serializer = serializers.HistorDetailSerializer(
            BookingHistory,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        bookingHistory = self.get_object(request, pk)
        print("bookingHistorybookingHistory", bookingHistory)
        if bookingHistory == None:
            raise PermissionDenied
        if request.user.is_superuser == False:
            if bookingHistory.booking.user != request.user:
                raise PermissionDenied

        bookingHistory.delete()

        return Response(status=HTTP_204_NO_CONTENT)
