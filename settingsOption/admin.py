from django.contrib import admin
from .models import SettingsOption


# Register your models here.
@admin.register(SettingsOption)
class SettingsOptionAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "name",
    )

    list_display_links = (
        "type",
        "name",
    )
