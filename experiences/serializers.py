from rest_framework.serializers import ModelSerializer
from .models import Experience, Perk
from categories.serializers import AddCategorySerializer
from rest_framework import serializers
from wishlists.models import Wishlist
from users.models import User
from photos.models import Photo


class SaveUserAvatarInExperienceSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = ("picture",)


class TinyUserInExperienceSerializer(ModelSerializer):
    avatar = SaveUserAvatarInExperienceSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "avatar",
        )


class TinyPhotoInExperienceSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "picture",
        )


class PhotoInExperienceSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "picture",
            "description",
        )


class TinyExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "created_at",
            "updated_at",
        )


class ExperienceCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    perks_id = serializers.ListField(child=serializers.IntegerField(read_only=True))
    total_available_guest = serializers.IntegerField(min_value=1)
    start = serializers.TimeField(required=False)
    end = serializers.TimeField(required=False)

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "address",
            "start",
            "end",
            "things_to_know",
            "perks_id",
            "category_id",
            "description",
            "total_available_guest",
        )


class ExperienceEditSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False, min_value=0)
    address = serializers.CharField(required=False)
    start = serializers.TimeField(required=False)
    end = serializers.TimeField(required=False)
    things_to_know = serializers.CharField(required=False)
    perks_id = serializers.ListField(child=serializers.IntegerField(), required=False)
    category_id = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)
    total_available_guest = serializers.IntegerField(required=False, min_value=0)

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "address",
            "start",
            "end",
            "things_to_know",
            "perks_id",
            "category_id",
            "description",
            "total_available_guest",
        )


class ExperienceListSerializer(serializers.ModelSerializer):
    experience_rating = (
        serializers.SerializerMethodField()
    )  # get_experience_rating 메소드이름 정해져있음! 필요로함!
    photos = TinyPhotoInExperienceSerializer(many=True, read_only=True)
    category = AddCategorySerializer()

    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, room):
        # request = self.context["request"] #이러면 없으면 애러뜸
        request = self.context.get("request")  # 이러면 없으면 애러뜸

        if request:
            if request.user.is_authenticated:
                # 2중필터 wishlist중 유저이름으로된것을 먼저 찾고 그중에 찾는룸이 있는지 볼수있다
                return Wishlist.objects.filter(
                    user=request.user,
                    rooms__pk=room.pk,
                ).exists()
        return False

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "photos",
            "price",
            "category",
            "created_at",
            "updated_at",
            "is_liked",
            "description",
            "experience_rating",
            "host",
        )

    # serializers.SerializerMethodField() 커스텀 하기위해 get_rating만들어야함
    def get_experience_rating(self, experience):
        return experience.experience_rating()


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = (
            "pk",
            "name",
            "details",
        )


class PerkDetailSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = (
            "pk",
            "name",
            "details",
            "explanation",
        )


class EditPerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = (
            "name",
            "details",
        )


class ExperienceDetailSerializer(serializers.ModelSerializer):
    experience_rating = (
        serializers.SerializerMethodField()
    )  # get_experience_rating 메소드이름 정해져있음! 필요로함!
    photos = PhotoInExperienceSerializer(many=True, read_only=True)
    category = AddCategorySerializer()
    perks = PerkSerializer(many=True)
    is_liked = serializers.SerializerMethodField()
    host = TinyUserInExperienceSerializer()

    def get_is_liked(self, experience):
        # request = self.context["request"] #이러면 없으면 애러뜸
        request = self.context.get("request")  # 이러면 없으면 애러뜸

        if request:
            if request.user.is_authenticated:
                # 2중필터 wishlist중 유저이름으로된것을 먼저 찾고 그중에 찾는룸이 있는지 볼수있다
                return Wishlist.objects.filter(
                    user=request.user,
                    experiences__pk=experience.pk,
                ).exists()
        return False

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "photos",
            "country",
            "city",
            "price",
            "address",
            "start",
            "end",
            "things_to_know",
            "perks",
            "category",
            "is_liked",
            "description",
            "total_available_guest",
            "host",
            "experience_rating",
            "total_experience_review",
        )

    # serializers.SerializerMethodField() 커스텀 하기위해 get_rating만들어야함
    def get_experience_rating(self, experience):
        return experience.experience_rating()
