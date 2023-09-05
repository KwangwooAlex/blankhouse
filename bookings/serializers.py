from django.utils import timezone
from rest_framework import serializers
from .models import Booking
from rooms.models import Room
from experiences.serializers import TinyExperienceSerializer
from rooms.serializers import TinyRoomSerializer, TinyRoomWithPictureSerializer
from users.serializers import TinyUserSerializer


class CreateRoomBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    # room = TinyRoomSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            # "room",
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):  # check_in 불려질때 검사를 자동으로 실행함 value= check_in임
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate_check_out(self, value):  # check_out 불려질때 검사를 자동으로 실행함 value= checkout임
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate(self, data):  # is_valid불려질때나옴 data는 모든 data를 들고있음
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out."
            )
        # print("data result", data)
        # print("context result", self.context.get("room"))
        if Booking.objects.filter(
            room=self.context.get("room"),
            check_in__lt=data["check_out"],
            check_out__gt=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of those dates are already taken."
            )
        return data


class PublicBookingSerializer(serializers.ModelSerializer):
    guests = serializers.IntegerField(required=False, min_value=1)
    room = TinyRoomWithPictureSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "pk",
            "room",
            "check_in",
            "check_out",
            "guests",
            "status",
            "total_cost",
            "created_at",
            "updated_at",
        )


class PublicBookingWithNameSerializer(serializers.ModelSerializer):
    guests = serializers.IntegerField(required=False, min_value=1)
    room = TinyRoomWithPictureSerializer(read_only=True)
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "pk",
            "room",
            "user",
            "check_in",
            "check_out",
            "guests",
            "status",
            "total_cost",
            "created_at",
            "updated_at",
        )


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    # experience = TinyExperienceSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            # "experience",
            "check_in",
            "guests",
        )

    def validate_check_in(self, value):  # check_in 불려질때 검사를 자동으로 실행함 value= check_in임
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    def validate(self, data):  # is_valid불려질때나옴 data는 모든 data를 들고있음
        current_total_guest = 0
        for each_booking_guests in Booking.objects.filter(
            check_in=data["check_in"],
            experience=self.context.get("experience"),
        ):
            current_total_guest += each_booking_guests.guests

        if (
            current_total_guest + data["guests"]
            > self.context.get("experience").total_available_guest
        ):
            raise serializers.ValidationError("It can't exceed maximum guests")

        return data


class PublicExperienceBookingSerializer(serializers.ModelSerializer):
    guests = serializers.IntegerField(required=False, min_value=1)
    experience = TinyExperienceSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "pk",
            "experience",
            "check_in",
            "check_out",
            "guests",
            "total_cost",
            "created_at",
            "updated_at",
        )


# class EditExperienceBookingSerializer(serializers.ModelSerializer):


class BookingDetailSerializer(serializers.ModelSerializer):
    guests = serializers.IntegerField(required=False, min_value=1)
    user = TinyUserSerializer(read_only=True)
    experience = TinyExperienceSerializer(read_only=True)
    room = TinyRoomWithPictureSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "pk",
            "user",
            "experience",
            "room",
            "check_in",
            "check_out",
            "guests",
            "total_cost",
            "created_at",
            "updated_at",
        )
