from django.db import models
from common.models import CommonModel


# models.Model 가장 기본 모델


class Room(CommonModel):

    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = "shared_room", "Shared Room"

    name = models.CharField(
        max_length=180,
        default="",
    )

    country = models.CharField(
        max_length=50,
        default="Canada",
    )
    city = models.CharField(
        max_length=80,
        default="Calgary",
    )
    price = models.PositiveIntegerField()
    cleaning_fee = models.PositiveIntegerField()

    number_of_room = models.PositiveIntegerField()
    number_of_toilet = models.PositiveIntegerField()
    number_of_bed = models.PositiveIntegerField()
    maximum_guests = models.PositiveIntegerField()

    description = models.TextField()
    address = models.CharField(
        max_length=250,
    )

    pet_friendly = models.BooleanField(
        default=True,
    )

    house_type = models.CharField(
        max_length=20,
        choices=RoomKindChoices.choices,
    )

    things_to_know = models.TextField(
        null=True,
        blank=True,
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )

    amenities = models.ManyToManyField(
        "rooms.Amenity",
        related_name="rooms",
    )

    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  # 카테고리가 삭제되도 room은 삭제되지 않음, 반대는 casacade
        related_name="rooms",
    )

    # admin에서 기본이름을 무엇으로 나타낼지 이렇게안하면 object자체로 이름이뜸
    # def __str__(self) -> str:
    #     return self.name

    # room 는 self가 될수있다 첫번째인자가 자기 자신이라는것만 알면됨
    def __str__(self) -> str:
        return self.name

    def total_amenities(self):
        return self.amenities.count()

    def rating(room):
        count = room.reviews.count()
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
            for review in room.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating / count, 2)


class Amenity(CommonModel):

    """Amenity Definiton"""

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"  # change the sub!! title in admin menu name


class AddOnService(CommonModel):

    """Amenity Definiton"""

    name = models.CharField(
        max_length=150,
    )
    description = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = (
            "AddOnServices"  # change the sub!! title in admin menu name
        )
