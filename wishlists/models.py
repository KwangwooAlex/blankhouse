from django.db import models
from common.models import CommonModel


class Wishlist(CommonModel):

    """Wishlist Model Definition"""

    # 위시리스트에서는 룸과 경험을 필수조건으로 함.. black=True하면 둘중 하나만 해도됨!
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="wishlists",
    )

    rooms = models.ManyToManyField(
        "rooms.Room",
        related_name="wishlists",
        null=True,
        blank=True,
    )

    experiences = models.ManyToManyField(
        "experiences.Experience",
        related_name="wishlists",
        null=True,
        blank=True,
    )

    def wishlist_count(self):
        countForRooms = self.rooms.count()
        countForExperience = self.experiences.count()
        return countForRooms + countForExperience

    # def __str__(self) -> str:
    #     if self.rooms:
    #         return self.rooms.na, e
    #     if self.experiences:
    #         return self.user.username
