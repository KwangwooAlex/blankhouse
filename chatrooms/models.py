from django.db import models
from common.models import CommonModel


class Chatroom(CommonModel):

    """Review from a User to a Room or Experience"""

    user = models.ManyToManyField(
        "users.User",
        related_name="chatroom",
    )

    def __str__(self) -> str:
        return f"{self.pk} - chatroom"

    def total_message(self):
        # print(
        #     "dir testing", dir(self.soldProduct.all().values("product").values("price"))
        # )
        total = 0
        # self.directMessage.count()
        return total
