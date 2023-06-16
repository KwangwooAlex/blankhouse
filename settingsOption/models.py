from django.db import models
from common.models import CommonModel


# Create your models here.
class SettingsOption(CommonModel):

    """Review from a User to a Room or Experience"""

    type = models.CharField(
        max_length=50,
        default="",
    )

    name = models.CharField(
        max_length=100,
        default="",
    )

    detail = models.TextField(
        max_length=1500,
        default="",
    )
