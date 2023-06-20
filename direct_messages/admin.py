from django.contrib import admin
from .models import DirectMessages


# Register your models here.
@admin.register(DirectMessages)
class DirectMessagesAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_display = (
        "pk",
        "__str__",  # model의 __str__것을 보여주고 싶으면 저렇게 쓰면됨 타이틀은 클래스 이름이 될것임 내용은 __str__
    )
    list_filter = (
        # 필터 순서가 중요하다 wordFilter가 최우선이 되고싶으면 맨위에 놓으면됨
        "user__username",
    )
