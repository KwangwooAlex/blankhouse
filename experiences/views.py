from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Perk, Experience
from bookings.models import Booking
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
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from bookings.serializers import (
    PublicExperienceBookingSerializer,
    CreateExperienceBookingSerializer,
)
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


class Perks(GenericAPIView):
    queryset = Perk.objects.all()  # 필수
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.PerkDetailSerializer
        return serializers.PerkSerializer

    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = serializers.PerkSerializer(
            all_perks,
            many=True,
            context={"request": request},
            # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
            # context에 접근할수있음
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.PerkDetailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():  # transaction 써줘야 만들다가 실패하면 rollback함
                    new_perk = serializer.save()
                    serializer = serializers.PerkDetailSerializer(
                        new_perk,
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


class PerkDetail(GenericAPIView):
    queryset = Perk.objects.all()  # 필수

    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        return serializers.PerkDetailSerializer

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkDetailSerializer(
            perk,
            context={"request": request},
            # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
            # context에 접근할수있음
        )
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.is_superuser:
            perk = self.get_object(pk)
            serializer = serializers.PerkDetailSerializer(
                perk,
                data=request.data,
                partial=True,  # 부분적으로만 업데이트 허용!
            )
            # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
            if serializer.is_valid():
                updated_perk = serializer.save()
                return Response(
                    serializers.PerkDetailSerializer(updated_perk).data,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )

    def delete(self, request, pk):
        perk = self.get_object(pk)

        if request.user.is_superuser == False:
            raise PermissionDenied

        perk.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class ExperienceBookings(GenericAPIView):
    queryset = Experience.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return CreateExperienceBookingSerializer
        return PublicExperienceBookingSerializer

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            check_in__gte=now,  # 현재보다 미래의 예약만 보여주고 싶음!
        )
        serializer = PublicExperienceBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(
            data=request.data,
            context={"experience": experience},
        )
        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicExperienceBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "check_in",
                openapi.IN_QUERY,
                description="check in time ex) 2023-06-06",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class ExperienceBookingCheck(GenericAPIView):
    queryset = Experience.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return CreateExperienceBookingSerializer
        # return PublicBookingSerializer

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        current_total_guest = 0
        check_in = request.query_params.get("check_in")
        for each_booking_guests in Booking.objects.filter(
            experience=experience,
            check_in=check_in,
        ):
            current_total_guest += each_booking_guests.guests
        return Response(
            {
                "total available guest for the experience in a day": experience.total_available_guest,
                "current total guest for this experience in the date": current_total_guest,
                "available guests": experience.total_available_guest
                - current_total_guest,
            }
        )

        # if exists:
        #     return Response({"ok": False})
        # return Response({"ok": True})
