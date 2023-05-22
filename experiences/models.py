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
