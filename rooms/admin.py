from django.contrib import admin
from .models import Room, Amenity, AddOnService

# Register your models here.


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        # 여기서는 values("price")사용하면 안됨. all을해야 함수가 내장된 room의 오브젝트가 올것임
        room.price = 0
        room.save()


# User admin과는 다른 우리가 커스텀한 모델 어드민임!!
# ModelAdmin
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)

    list_display = (
        "pk",
        "name",
        "price",
        "house_type",
        "rating",
        "owner",
        "total_amenities",
        "created_at",
    )

    list_display_links = (
        "name",
        "price",
        "house_type",
    )  # 이 column은 누르면 디테일 볼수있게함

    list_filter = (
        "country",
        "city",
        "pet_friendly",
        "house_type",
        "amenities",
        "created_at",
        "updated_at",
    )

    search_fields = (
        # 설정을 안해주면 기본은 contain을 적용한 search가 됨
        # ^붙이면 startwith임
        "name",
        "^price",
        "=owner__username",  # 방이름을 유저이름으로 검색하고싶을떄는 __만 붙이면 user(owner)이용가능!
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    # 그냥 두면 생성,업데이트 날짜가 보이지 않는데, 이걸통해 detail페이지에도 보여줄수있다
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(AddOnService)
class AddOnServiceAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    # 그냥 두면 생성,업데이트 날짜가 보이지 않는데, 이걸통해 detail페이지에도 보여줄수있다
    readonly_fields = (
        "created_at",
        "updated_at",
    )
