from django.db import models
from common.models import CommonModel


class Experience(CommonModel):

    """Experience Model Definiiton"""

    country = models.CharField(
        max_length=50,
        default="Cananda",
    )
    city = models.CharField(
        max_length=80,
        default="Calgary",
    )
    name = models.CharField(
        max_length=250,
    )
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=250,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField(
        null=True,
        blank=True,
    )
    things_to_know = models.TextField(
        null=True,
        blank=True,
    )
    perks = models.ManyToManyField(
        "experiences.Perk",
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  # 카테고리가 삭제되도 experience는 삭제되지 않음, 반대는 casacade
        related_name="experiences",
    )

    def __str__(self) -> str:
        return self.name

    def total_perks(self):
        return self.perks.count()

    def rating(experience):
        count = experience.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            # room에서 바로 review접근 가능함, review에서 포린키 연결했거 related_name 해놔서
            # all().values("rating") 안쓰고 그냥 all()만 쓰면 필요없는 정보까지 다 가져올것임
            # values("rating")을 써줘야 rating에관한 정보만 가져올것임
            # 문제는 review가 객체가 아니라서 review.rating 대신 review["rating"]을 해야함
            # 리스트로 받아온다 [{review:"4"},{review:"3"}] 이렇게..
            # value()를 안썼다면 [<object room1>,<object room2>] 이렇게 객체의 어레이가 왔을것임
            for review in experience.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)


class Perk(CommonModel):

    """What is included on an Experience"""

    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    explanation = models.TextField(
        blank=True,
        default="",
    )

    def __str__(self) -> str:
        return self.name
