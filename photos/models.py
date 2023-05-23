from django.db import models
from common.models import CommonModel
from .validators import validate_file_size

# Create your models here.


class Photo(CommonModel):
    picture = models.FileField(upload_to="media/", validators=[validate_file_size])
    description = models.CharField(max_length=140, blank=True, null=True)
    # pdf = models.FileField(upload_to='pdfs')
    # photos = models.ImageField(upload_to='photos')
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="avatar",
    )

    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def displayURL(self):
        return self.picture.url

    def __str__(self) -> str:
        if self.user:
            return f"Photo for {self.user} Avatar"
        if self.room:
            return f"Photo for {self.room}"
        if self.experience:
            return f"Photo for {self.experience}"
