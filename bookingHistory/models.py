from django.db import models
from common.models import CommonModel


class BookingHistory(CommonModel):

    """Booking Model Definition"""

    booking = models.OneToOneField(
        "bookings.Booking",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="bookingHistory",
    )

    service_fee = models.PositiveIntegerField(default=0)
    room_fee = models.PositiveIntegerField(default=0)
    cleaning_fee = models.PositiveIntegerField(default=0)
    experience_fee = models.PositiveIntegerField(default=0)
    tax = models.PositiveIntegerField(default=0)
    final_total_cost = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.booking.kind == "room":
            return f"`{self.booking.room}` booking history for: {self.booking.user.username}"
        if self.booking.kind == "experience":
            return f"`{self.booking.experience}` booking history for: {self.booking.user.username}"

    def total_cost(self):
        if self.booking.kind == "room":
            total_price = (
                self.service_fee + self.room_fee + self.cleaning_fee + self.tax
            )
            return f"{total_price}"
        if self.booking.kind == "experience":
            total_price = self.experience_fee * self.tax
            return f"{total_price}"
