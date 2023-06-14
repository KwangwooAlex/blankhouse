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
from categories.models import Category

# Create your views here.


class Experiences(GenericAPIView):
    queryset = Experience.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.ExperienceCreateSerializer
        return serializers.ExperienceListSerializer

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = serializers.ExperienceListSerializer(
            all_experiences,
            many=True,
            context={"request": request},
            # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
            # context에 접근할수있음
        )
        return Response(serializer.data)

    def post(self, request):
        #  if request.user.is_authenticated: 위에서 검사해준다
        serializer = serializers.ExperienceCreateSerializer(data=request.data)
        if serializer.is_valid():
            # read_only=True 를 serializer에 써줘야 내가 원하는 이름의 변수를body로 받을수있다
            # ex) post room 에서 category_id 랑 amenities_id가 안되서 read_only 사용하니 받아줌
            category_id = request.data.get("category_id")

            if not category_id:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_id)

                # 카테고리가 두종류로 정했다 하나는 experience 하나는 room을 위한것
                # 우리는 룸을 위한 kind만 받아줄거기때문에 한번더 체크한다
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The category kind should be 'EXPERIENCES'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")

            # owner = request.user는 serialier의 create(self, validated_data)의 validated_data에 추가될것임 create는 이미 상속받아져있기에 내장되어있다
            # 즉 data는 request.data+ owner = request.user 이 함께 전송된다
            # room = serializer.save(
            #     owner=request.user,
            #     category=category,
            # )

            # amenities = request.data.get("amenities")
            # for amenity_pk in amenities:
            #     try:
            #         amenity = Amenity.objects.get(pk=amenity_pk)
            #     except Amenity.DoesNotExist:
            #         room.delete()
            #         raise ParseError(f"Amenity with id {amenity_pk} not found")
            #     # room은 여러개의 어메니티를 가질수있으므로 add 가 가능! 하나만 가질수있을때만
            #     # = <- 써서 해야함 밑에와같이!
            #     # room = serializer.save(
            #     # owner=request.user,
            #     # category=category,
            #     room.amenities.add(amenity)  # or remove()도 가능

            # serializer = RoomDetailSerializer(room)
            # return Response(serializer.data)

            # 위의 방법으로 일일히 체크하지말고 transaction을 이용하면 쿼리 3개가 예를들어 실행될때
            # 하나라도 오류가 있다면 나머지 2개의 쿼리도 다 취소시켜 버린다!
            # 모의로 쿼리를 실행시켜보고 제대로될시 db에 반영해서 db가 힘들지 않음
            try:
                with transaction.atomic():
                    # 1 쿼리
                    experience = serializer.save(
                        host=request.user,
                        category=category,
                    )

                    perks_id = request.data.get("perks_id")

                    # 2쿼리
                    for perk_pk in perks_id:
                        perks = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perks)

                    serializer = serializers.ExperienceDetailSerializer(
                        experience,
                        context={"request": request},
                    )

                    return Response(serializer.data)
            except Exception:
                # transaction 이 실패하면 에러를 낼것임
                raise ParseError("Perks not found")
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class ExperienceDetail(GenericAPIView):
    queryset = Experience.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.ExperienceEditSerializer
        return serializers.ExperienceDetailSerializer

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        Experience = self.get_object(pk)

        serializer = serializers.ExperienceDetailSerializer(
            Experience,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.is_superuser:
            experience = self.get_object(pk)

            serializer = serializers.ExperienceEditSerializer(
                experience,
                data=request.data,
                partial=True,  # 부분적으로만 업데이트 허용!
            )
            # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
            if serializer.is_valid():
                updated_experience = serializer.save()

                if request.data.get("perks_id"):
                    updated_experience.perks.clear()
                    perks = request.data.get("perks_id")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        updated_experience.perks.add(perk)

                return Response(
                    serializers.ExperienceDetailSerializer(updated_experience).data,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )
        return Response(status=HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        if request.user.is_superuser:
            experience = self.get_object(pk)
            experience.delete()

            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_401_UNAUTHORIZED)


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
