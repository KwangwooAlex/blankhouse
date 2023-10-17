from django.contrib import admin
from .models import Feedback, Answer


@admin.register(Feedback)
class Feedback(admin.ModelAdmin):
    list_display = (
        "pk",
        "kind",
        "writer",
        "status",
        "created_at",
    )

    # list_filter = ("category",)


@admin.register(Answer)
class Answer(admin.ModelAdmin):
    list_display = (
        "pk",
        "writer",
        "details",
        "feedback",
        "created_at",
    )
