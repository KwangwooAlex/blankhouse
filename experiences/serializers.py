from rest_framework.serializers import ModelSerializer
from .models import Experience, Perk
from categories.serializers import AddCategorySerializer
from rest_framework import serializers
from wishlists.models import Wishlist


class ExperienceListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()  # get_rating 메소드이름 정해져있음! 필요로함!
    # photos = PhotoSerializer(many=True, read_only=True)
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
            # "photos",
            "price",
            "category",
            "created_at",
            "updated_at",
            "is_liked",
            "description",
            "rating",
        )

    # serializers.SerializerMethodField() 커스텀 하기위해 get_rating만들어야함
    def get_rating(self, room):
        return room.rating()


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
