from django.contrib import admin
from .models import UserNotifications


# Register your models here.
@admin.register(UserNotifications)
class UserNotificationsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "type",
        "name",
        "user",
    )

    list_display_links = (
        "type",
        "name",
    )
