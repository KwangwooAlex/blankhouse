from django.db import models
from common.models import CommonModel


class Review(CommonModel):

    """Review from a User to a Room or Experience"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,  # room이나 experience에 리뷰가 보내질수있으므로 둘중하나는 null 이 가능함
        on_delete=models.CASCADE,  # user 지워지면 review도 사라짐
        related_name="reviews",
    )

    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,  # room이나 experience에 리뷰가 보내질수있으므로 둘중하나는 null 이 가능함
        on_delete=models.CASCADE,  # user 지워지면 review도 사라짐
        related_name="reviews",
    )

    payload = models.TextField()  # 내용
    rating = models.PositiveIntegerField()

    def Room_Name(self):
        if self.room:
            return self.room.name

    def Experience_Name(self):
        if self.experience:
            return self.experience.name

    def __str__(self) -> str:
        return f"{self.user} / {self.rating}⭐️"
