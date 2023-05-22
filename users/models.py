from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_file_size


# AbstractUser 의 경로에 있는 User class말고 우리가 커스텀 한걸 쓰기위해서는
# setting.py에서 다른 경로를 설정 해주어야한다
class User(AbstractUser):
    # 오버라이딩을 하여 성, 이름을 사용하지않고 하나의 name 이라는 새로운 필드를 커스텀한다(상속에서 오버라이딩)

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")  # 첫번쨰는 디비에 들어갈 value 두번째는 admin패널에 보일 내용
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won"
        USD = "usd", "Dollar"

    password = models.CharField(max_length=128)
    avatar = models.FileField(
        upload_to="media/", validators=[validate_file_size], blank=True, null=True
    )

    # username 은 AbstractUser 상속받은곳에서 가져올것임
    email = models.CharField(max_length=150, blank=True, null=True)
    balance = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=150, blank=True, null=True)
    emergency_contact = models.CharField(max_length=11, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    is_host = models.BooleanField(default=False)
    born_year = models.CharField(max_length=30, blank=True, null=True)
    school = models.CharField(max_length=40, blank=True, null=True)
    work = models.CharField(max_length=40, blank=True, null=True)
    hobby = models.CharField(max_length=50, blank=True, null=True)

    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )
