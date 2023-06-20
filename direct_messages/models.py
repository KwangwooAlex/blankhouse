from django.db import models
from common.models import CommonModel


class DirectMessages(CommonModel):

    """Review from a User to a Room or Experience"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="directMessage",
    )

    chatroom = models.ForeignKey(
        "chatrooms.Chatroom",
        on_delete=models.CASCADE,
        related_name="directMessage",
    )

    payload = models.TextField(max_length=300)  # 내용

    def __str__(self) -> str:
        return f"User - {self.user} / ChatRoom - {self.chatroom.pk} "
