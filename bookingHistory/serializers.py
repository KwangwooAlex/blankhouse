from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.serializers import TinyUserSerializer
from bookings.serializers import BookingDetailSerializer
from .models import BookingHistory


class RoomBookingHistorySerializer(ModelSerializer):
    booking = BookingDetailSerializer(read_only=True)

    class Meta:
        model = BookingHistory
        fields = (
            "pk",
            "booking",
            "total_cost",
            "final_total_cost",
            "created_at",
            "updated_at",
        )


class HistorDetailSerializer(ModelSerializer):
    booking = BookingDetailSerializer(read_only=True)

    class Meta:
        model = BookingHistory
        fields = (
            "pk",
            "booking",
            "service_fee",
            "room_fee",
            "cleaning_fee",
            "tax",
            "total_cost",
            "final_total_cost",
            "created_at",
            "updated_at",
        )


class CreateBookingHistorSerializer(ModelSerializer):
    booking_id = serializers.IntegerField(required=True)

    class Meta:
        model = BookingHistory
        fields = (
            "pk",
            "booking_id",
            "service_fee",
            "room_fee",
            "cleaning_fee",
            "final_total_cost",
            "tax",
            "created_at",
            "updated_at",
        )


# ----- ----- ----- ----- ----- experience Serializer ----- ----- ----- -----
class ExperienceBookingHistorySerializer(ModelSerializer):
    booking = BookingDetailSerializer(read_only=True)

    class Meta:
        model = BookingHistory
        fields = (
            "pk",
            "booking",
            "total_cost",
            "created_at",
            "updated_at",
        )


class ExperienceHistorDetailSerializer(ModelSerializer):
    booking = BookingDetailSerializer(read_only=True)

    class Meta:
        model = BookingHistory
        fields = (
            "pk",
            "booking",
            "experience_fee",
            "tax",
            "total_cost",
            "final_total_cost",
            "created_at",
            "updated_at",
        )


class CreateExperienceBookingHistorSerializer(ModelSerializer):
    booking_id = serializers.IntegerField(required=True)

    class Meta:
        model = BookingHistory
        fields = (
            "pk",
            "booking_id",
            "experience_fee",
            "tax",
            "final_total_cost",
            "created_at",
            "updated_at",
        )


# class ExperienceBookingHistorySerializer(ModelSerializer):
#     # soldProduct = SoldProductSerializer(many=True, read_only=True)
#     # user = TinyUserSerializer(read_only=True)
#     # order = OrderDetailSerializer(read_only=True)

#     class Meta:
#         model = BookingHistory
#         fields = (
#             "pk",
#             "user",
#             "order",
#             "total_order_price",
#             "created_at",
#             "updated_at",
#             # "",
#             # "description",
#         )
