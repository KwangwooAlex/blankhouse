from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Amenity, Room
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
from drf_yasg.utils import swagger_auto_schema
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from categories.models import Category
from django.db.models import Avg, Sum, Count

# Create your views here.


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "keyword",
                openapi.IN_QUERY,
                description="Search by keyword",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "owner_name",
                openapi.IN_QUERY,
                description="Search by owner name",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "country",
                openapi.IN_QUERY,
                description="Search by country",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "city",
                openapi.IN_QUERY,
                description="Search by city",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "category",
                openapi.IN_QUERY,
                description="filter by category / default any",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "rating",
                openapi.IN_QUERY,
                description="filter by rating / default any ex) rating<=result",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "house_type",
                openapi.IN_QUERY,
                description="filter by house_type / default any  ex) Entire Place",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "number_of_bedrooms",
                openapi.IN_QUERY,
                description="filter by house_type / default any ex) 1",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "number_of_beds",
                openapi.IN_QUERY,
                description="filter by house_type / default any ex) 1",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "number_of_toilets",
                openapi.IN_QUERY,
                description="filter by number_of_toilets / default any ex) 1",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "maximum_guests",
                openapi.IN_QUERY,
                description="filter by maximum_guests / default any ex) maximum_guests < result",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "mininum_price",
                openapi.IN_QUERY,
                description="filter by mininum_price / minimum <= result",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "maximum_price",
                openapi.IN_QUERY,
                description="filter by maximum_price / maximum >= result",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "check_in",
                openapi.IN_QUERY,
                description="check in and check out must exist for filter / ex) 2023-06-06",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "check_out",
                openapi.IN_QUERY,
                description="check in and check out must exist for filter / ex) 2023-06-16",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "per_page",
                openapi.IN_QUERY,
                description="default 12",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="default 1",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class Rooms(GenericAPIView):
    queryset = Room.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return serializers.RoomCreateSerializer
        return serializers.RoomListSerializer

    def get(self, request):
        all_rooms = Room.objects.all()
        all_rooms = (
            all_rooms.filter(name__contains=request.query_params.get("keyword"))
            if request.query_params.get("keyword")
            else all_rooms
        )

        all_rooms = (
            all_rooms.filter(owner__username=request.query_params.get("owner_name"))
            if request.query_params.get("owner_name")
            else all_rooms
        )

        all_rooms = (
            all_rooms.filter(country__contains=request.query_params.get("country"))
            if request.query_params.get("country")
            else all_rooms
        )

        all_rooms = (
            all_rooms.filter(city__contains=request.query_params.get("city"))
            if request.query_params.get("city")
            else all_rooms
        )

        all_rooms = (
            all_rooms.filter(category__name=request.query_params.get("category"))
            if request.query_params.get("category")
            else all_rooms
        )

        # https://stackoverflow.com/questions/59479908/how-to-make-an-average-from-values-of-a-foreign-key-in-django
        # 위에 사이트에서 참고함... rating을 모델에서 aggregate로 추가해준뒤 (월래 def는 필터 안되기에 여기서 annotate로 avg_rating을 강제로 넣어줘서
        # 필터하게끔 해준다!
        all_rooms = (
            all_rooms.annotate(avg_rating=Avg("reviews__rating")).filter(
                avg_rating__gte=request.query_params.get("rating")
            )
            if request.query_params.get("rating")
            else all_rooms
        )

        all_rooms = (
            all_rooms.filter(house_type=request.query_params.get("house_type"))
            if request.query_params.get("house_type")
            else all_rooms
        )

        all_rooms = (
            all_rooms.filter(
                number_of_room=request.query_params.get("number_of_bedrooms")
            )
            if request.query_params.get("number_of_bedrooms")
            else all_rooms
        )

        all_rooms = (
            all_rooms.filter(number_of_bed=request.query_params.get("number_of_beds"))
            if request.query_params.get("number_of_beds")
            else all_rooms
        )

        all_rooms = (
            all_rooms.filter(
                number_of_toilet=request.query_params.get("number_of_toilets")
            )
            if request.query_params.get("number_of_toilets")
            else all_rooms
        )

        all_rooms = (
            all_rooms.filter(price__gte=request.query_params.get("mininum_price"))
            if request.query_params.get("mininum_price")
            else all_rooms
        )

        all_rooms = (
            all_rooms.filter(price__lte=request.query_params.get("maximum_price"))
            if request.query_params.get("maximum_price")
            else all_rooms
        )

        all_rooms = (
            all_rooms.filter(
                maximum_guests__gte=request.query_params.get("maximum_guests")
            )
            if request.query_params.get("maximum_guests")
            else all_rooms
        )

        all_rooms = (
            all_rooms.exclude(
                bookings__in=Booking.objects.filter(
                    check_in__lt=request.query_params.get("check_out"),
                    check_out__gt=request.query_params.get("check_in"),
                )
            )
            if (
                request.query_params.get("check_in")
                and request.query_params.get("check_out")
            )
            else all_rooms
        )

        per_page = (
            request.query_params.get("per_page")
            if request.query_params.get("per_page")
            else 12
        )
        page = (
            request.query_params.get("page") if request.query_params.get("page") else 1
        )
        try:
            # all_rooms order_by없이 넣으면 경고뜸
            paginator = Paginator(all_rooms.order_by("id"), per_page)
            paginated_all_rooms_result = paginator.page(page)
        except EmptyPage:
            raise ParseError("Room not found")

        serializer = serializers.RoomListSerializer(
            paginated_all_rooms_result,
            many=True,
            context={"request": request},
            # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
            # context에 접근할수있음
        )

        # return Response(serializer.data)
        return Response(
            {
                "page_size": per_page,
                "total_objects": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page_number": page,
                "results": serializer.data,
            }
        )

    def post(self, request):
        #  if request.user.is_authenticated: 위에서 검사해준다
        serializer = serializers.RoomCreateSerializer(data=request.data)
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
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be 'rooms'")
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
                    print("categorycategory", category)
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )

                    amenities = request.data.get("amenities_id")

                    # 2쿼리
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)

                    serializer = serializers.RoomDetailSerializer(
                        room,
                        context={"request": request},
                    )

                    return Response(serializer.data)
            except Exception:
                # transaction 이 실패하면 에러를 낼것임
                raise ParseError("Amenity not found")
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomDetail(GenericAPIView):
    queryset = Room.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.RoomEditSerializer
        return serializers.RoomDetailSerializer

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        Room = self.get_object(pk)

        serializer = serializers.RoomDetailSerializer(
            Room,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.is_superuser:
            room = self.get_object(pk)

            serializer = serializers.RoomEditSerializer(
                room,
                data=request.data,
                partial=True,  # 부분적으로만 업데이트 허용!
            )
            # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
            if serializer.is_valid():
                updated_room = serializer.save()

                if request.data.get("amenities_id"):
                    updated_room.amenities.clear()
                    amenities = request.data.get("amenities_id")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        updated_room.amenities.add(amenity)

                return Response(
                    serializers.RoomDetailSerializer(updated_room).data,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )
        return Response(status=HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        if request.user.is_superuser:
            room = self.get_object(pk)
            room.delete()

            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_401_UNAUTHORIZED)


class Amenities(GenericAPIView):
    queryset = Amenity.objects.all()  # 필수
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        return serializers.AmenitySerializer

    @swagger_auto_schema(
        # request_body=serializers.EditAmenitySerializer,
        tags=["Amenities"],
        operation_id="This is testing api ID 111",
        operation_summary="This is swagger description testing text",
        operation_description="Modify Amenity detail",
        # deprecated=True,
    )
    def get(self, request):
        all_room_categories = Amenity.objects.all()
        serializer = serializers.AmenitySerializer(
            all_room_categories,
            many=True,
            context={"request": request},
            # 여기의 context를 이용하여 원하는 메소드 어떤것이든 시리얼라이저의
            # context에 접근할수있음
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        # request_body=serializers.EditAmenitySerializer,
        tags=["Amenities"],
        operation_id="This is testing api ID 1222",
        operation_summary="This is swagger description testing text",
        operation_description="Modify Amenity detail",
        # deprecated=True,
    )
    def post(self, request):
        serializer = serializers.AmenitySerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():  # transaction 써줘야 만들다가 실패하면 rollback함
                    newAmenity = serializer.save()
                    serializer = serializers.AmenitySerializer(
                        newAmenity,
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


class RoomBookings(GenericAPIView):
    queryset = Room.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return CreateRoomBookingSerializer
        return PublicBookingSerializer

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        print("room", room)
        # now = timezone.localtime(timezone.now()).date()
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            # check_in__gt=now,  # 현재보다 미래의 예약만 보여주고 싶음!
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(
            data=request.data,
            context={"room": room},
        )
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)
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
            openapi.Parameter(
                "check_out",
                openapi.IN_QUERY,
                description="check out time ex) 2023-06-06",
                type=openapi.TYPE_STRING,
            ),
        ]
    ),
)
class RoomBookingCheck(GenericAPIView):
    queryset = Room.objects.all()  # 필수
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return CreateRoomBookingSerializer
        # return PublicBookingSerializer

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        check_in = request.query_params.get("check_in")
        check_out = request.query_params.get("check_out")
        print("check IN", check_in)
        exists = Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()
        if exists:
            return Response({"ok": False})
        return Response({"ok": True})


# @method_decorator(
#     name="get",
#     decorator=swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 "check_in",
#                 openapi.IN_QUERY,
#                 description="check in time ex) 2023-06-06",
#                 type=openapi.TYPE_STRING,
#             ),
#             openapi.Parameter(
#                 "check_out",
#                 openapi.IN_QUERY,
#                 description="check out time ex) 2023-06-06",
#                 type=openapi.TYPE_STRING,
#             ),
#         ]
#     ),
# )
# class AllRoomBookings(GenericAPIView):
#     queryset = Room.objects.all()  # 필수
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get_serializer_class(self, *args, **kwargs):
#         if self.request.method == "POST":
#             return CreateRoomBookingSerializer
#         return PublicBookingSerializer

#     def get_object(self):
#         try:
#             return Room.objects.all()
#         except:
#             raise NotFound

#     def get(self, request):
#         check_in = request.query_params.get("check_in")
#         check_out = request.query_params.get("check_out")
#         all_room = Room.objects.all()
#         # now = timezone.localtime(timezone.now()).date()
#         # print("all_roomall_room1111", all_room)
#         # print("all_roomall_room10------", dir(all_room))

#         all_room = Room.objects.exclude(
#             bookings__in=Booking.objects.filter(
#                 check_in__lt=check_out, check_out__gt=check_in
#             )
#         )
#         #  위의식은 밑에껄 제대로 나타냄.. filter reverse 는 exclude가 아님!!
#         # all_room = Room.objects.exclude(
#         #     bookings__check_in__lt=check_out, bookings__check_out__gt=check_in
#         # )
#         # .distinct()

#         print("all_roomall_room2222", all_room)
#         serializer = serializers.RoomListSerializer(all_room, many=True)
#         return Response(serializer.data)


class AmenityDetail(GenericAPIView):
    queryset = Amenity.objects.all()  # 필수

    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # 유저검사 get은허용 delete put post는 유저인증된사라만 가능! 다른기능은 없음

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "PUT":
            return serializers.EditAmenitySerializer

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        # request_body=serializers.EditAmenitySerializer,
        tags=["Amenities"],
        operation_id="This is testing api ID 22222",
        operation_summary="This is swagger description testing text",
        operation_description="Modify Amenity detail",
        # deprecated=True,
    )
    def put(self, request, pk):
        if request.user.is_superuser:
            amenity = self.get_object(pk)
            serializer = serializers.EditAmenitySerializer(
                amenity,
                data=request.data,
                partial=True,  # 부분적으로만 업데이트 허용!
            )
            # save() 는 update or create 중 알아서 serializer가 메소드를 이다음 실행시켜줌
            if serializer.is_valid():
                updated_amenity = serializer.save()
                return Response(
                    serializers.AmenitySerializer(updated_amenity).data,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )

    @swagger_auto_schema(
        # request_body=serializers.EditAmenitySerializer,
        tags=["Amenities"],
        operation_id="This is testing api ID 3333",
        operation_summary="This is swagger description testing text",
        operation_description="Modify Amenity detail",
        # deprecated=True,
    )
    def delete(self, request, pk):
        amenity = self.get_object(pk)

        if request.user.is_superuser == False:
            raise PermissionDenied

        amenity.delete()

        return Response(status=HTTP_204_NO_CONTENT)
