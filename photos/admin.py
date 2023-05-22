from django.contrib import admin
from .models import Photo

# Register your models here.


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "__str__",  # model의 __str__것을 보여주고 싶으면 저렇게 쓰면됨 타이틀은 클래스 이름이 될것임 내용은 __str__
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = ("created_at", "updated_at", "displayURL")
