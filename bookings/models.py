from django.db import models
from common.models import CommonModel


class Booking(CommonModel):

    """Booking Model Definition"""

    class BookingKindChoices(models.TextChoices):
        ROOM = "room", "Room"
        EXPERIENCE = "experience", "Experience"

    class BookingStatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        ONGOING = "ongoing", "Ongoing"
        COMPLETED = "completed", "Completed"
        CANCELED = "canceled", "Canceled"

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
    status = models.CharField(
        max_length=15, choices=BookingStatusChoices.choices, default="pending"
    )

    # 시간 example
    # class UserData(models.Model):
    # uid = models.CharField(max_length=100)
    # email = models.CharField(max_length=100)
    # start_date = models.DateField(auto_now_add=True,editable=False)
    # end_date = models.DateTimeField(auto_now=True)

    # @property
    # def duration(self):
    #     if not (self.start_date and self.end_date):
    #         return None
    #     a,b=self.start_date, self.end_date
    #     return '%s:%s' % ((b-a).days*24 + (b-a).seconds//3600, (b-a).seconds%3600//60)

    def __str__(self):
        return f"{self.kind.title()} booking for: {self.user}"

    def total_cost(self):
        if self.room:
            total_price = (
                self.room.price * (self.check_out - self.check_in).days
                + self.room.cleaning_fee
            )
            return f"{total_price}"
        if self.experience:
            total_price = self.experience.price * self.guests
            return f"{total_price}"
