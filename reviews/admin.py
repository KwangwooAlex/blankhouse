from django.contrib import admin
from .models import Review

# Register your models here.


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"  # 필터 제목

    parameter_name = "parameter"  # url에 보낼 이름일뿐 queryset word랑은 다름!

    # lookups과 queryset은 필수이다!
    # 인자 갯수는 필수로 적어줘야함!
    # 필터할수있는 요소들을 설정함
    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    # 어떻게 필터할것인지 정하면됨
    def queryset(self, request, reviews):
        # request.GET 을통해서도 parameter를 가져올수있음!
        # 세번째 인자는 이전에 남은 결과들을 가져온다. 맨처음이면 모든 review의 리스트를 가져온다

        word = self.value()
        print("parameter word", word)
        if word:
            return reviews.filter(payload__contains=word)
        else:
            reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "__str__",  # model의 __str__것을 보여주고 싶으면 저렇게 쓰면됨 타이틀은 클래스 이름이 될것임 내용은 __str__
        # "payload",
        "Room_Name",
        "Experience_Name",
        "rating",
        "communication_rating",
        "location_rating",
        "accuracy_rating",
        "check_in_rating",
        "cleanliness_rating",
        "experience_rating",
    )
    list_filter = (
        # 필터 순서가 중요하다 wordFilter가 최우선이 되고싶으면 맨위에 놓으면됨
        WordFilter,
        "rating",
        "user__username",
        "room__name",
        "experience__name",
    )
