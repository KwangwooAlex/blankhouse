from django.db import models
from common.models import CommonModel


class Booking(CommonModel):

    """Booking Model Definition"""

    class BookingKindChoices(models.TextChoices):
        ROOM = "room", "Room"
        EXPERIENCE = "experience", "Experience"

    kind = models.CharField(
        max_length=15,
        choices=BookingKindChoices.choices,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,  # booking은 room과 experience중 하나를 가질수있음
        on_delete=models.SET_NULL,
        related_name="bookings",
    )

    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bookings",
    )

    # 투어는 check_in만 설정하자!
    check_in = models.DateField(
        null=True,
        blank=True,
    )
    check_out = models.DateField(
        null=True,
        blank=True,
    )

    # 투어는 시간이 필요없다, 단지 날짜만 필요!
    # experience_time = models.DateTimeField(
    #     null=True,
    #     blank=True,
    # )
    guests = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.kind.title()} booking for: {self.user}"
