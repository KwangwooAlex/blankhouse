from django.utils import timezone
from rest_framework import serializers
from .models import Booking
from rooms.models import Room


class CreateRoomBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
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

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )
