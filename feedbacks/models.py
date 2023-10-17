from django.db import models
from common.models import CommonModel


class Feedback(CommonModel):

    """Experience Model Definiiton"""

    class FeedbackStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"

    kind = models.CharField(
        max_length=50,
    )

    writer = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )

    details = models.TextField()

    status = models.CharField(
        max_length=15, choices=FeedbackStatus.choices, blank=True, null=True
    )

    def __str__(self) -> str:
        return "PK:{} / {} / {}".format(self.pk, self.writer.username, self.created_at)


class Answer(CommonModel):

    """What is included on an Experience"""

    details = models.TextField()
    writer = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="answers",
    )

    feedback = models.ForeignKey(
        "feedbacks.Feedback",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="answers",
    )

    def __str__(self) -> str:
        return "PK:{} / {} / {}".format(
            self.feedback.pk, self.writer.username, self.created_at
        )
