from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# 유저 model을 등록시킬것임
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "avatar",
                    "username",
                    "password",
                    "email",
                    "is_host",
                    "emergency_contact",
                    "gender",
                    "language",
                    "currency",
                    "born_year",
                    "school",
                    "work",
                    "hobby",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
                # 처음에 보여줄지안보여줄지
                "classes": ("collapse",),
            },
        ),
    )

    list_display = ("pk", "username", "email", "is_host", "is_superuser")
