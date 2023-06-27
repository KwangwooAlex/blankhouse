from django.contrib import admin
from .models import BookingHistory


@admin.register(BookingHistory)
class BookingHistory(admin.ModelAdmin):
    list_display = (
        "pk",
        "__str__",
        "booking",
        # "total_cost",
    )
    list_filter = ("booking",)
