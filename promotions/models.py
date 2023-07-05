from django.db import models
from common.models import CommonModel


# Create your models here.
class Promotion(CommonModel):

    """Review from a User to a Room or Experience"""

    users = models.ManyToManyField(
        "users.User",
        related_name="promotion",
    )

    name = models.CharField(
        max_length=180,
        default="Normal promotion",
    )

    description = models.CharField(
        max_length=300,
        default="Basic Promotion",
    )

    discount_rate = models.PositiveIntegerField(default=0)

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.discount_rate}%"
