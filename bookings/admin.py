from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class Booking(admin.ModelAdmin):
    list_display = (
        "pk",
        "__str__",
        "kind",
        "user",
        "room",
        "experience",
        "status",
        "check_in",
        "check_out",
        "guests",
        "total_cost",
    )
    list_filter = ("kind",)
