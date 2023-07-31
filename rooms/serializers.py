from rest_framework.serializers import ModelSerializer
from .models import Room, Amenity
from users.models import User
from photos.models import Photo
from rest_framework import serializers
from categories.serializers import AddCategorySerializer
from wishlists.models import Wishlist


class SaveUserAvatarInRoomSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = ("picture",)


class TinyUserInRoomSerializer(ModelSerializer):
    avatar = SaveUserAvatarInRoomSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "avatar",
        )


class TinyPhotoInRoomSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "picture",
        )


class PhotoInRoomSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "picture",
            "description",
        )


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "pk",
            "name",
            "description",
        )


class EditAmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class TinyRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "created_at",
            "updated_at",
        )

    # serializers.SerializerMethodField() 커스텀 하기위해 get_rating만들어야함
    def get_rating(self, room):
        return room.rating()


class RoomCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    amenities_id = serializers.ListField(child=serializers.IntegerField(read_only=True))

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "cleaning_fee",
            "number_of_room",
            "number_of_toilet",
            "number_of_bed",
            "maximum_guests",
            "address",
            "pet_friendly",
            "house_type",
            "things_to_know",
            "category_id",
            "amenities_id",
            "description",
        )


class RoomEditSerializer(serializers.ModelSerializer):
    ROOM_KIND_CHOICES = (
        ("entire_place", "Entire Place"),
        ("private_room", "Private Room"),
        ("shared_room", "Shared Room"),
    )

    category_id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False, min_value=0)
    cleaning_fee = serializers.IntegerField(required=False, min_value=0)
    number_of_room = serializers.IntegerField(required=False, min_value=0)
    number_of_toilet = serializers.IntegerField(required=False, min_value=0)
    number_of_bed = serializers.IntegerField(required=False, min_value=0)
    maximum_guests = serializers.IntegerField(required=False, min_value=0)
    address = serializers.CharField(required=False)
    amenities_id = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    pet_friendly = serializers.BooleanField(required=False)
    house_type = serializers.ChoiceField(required=False, choices=ROOM_KIND_CHOICES)
    things_to_know = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "cleaning_fee",
            "number_of_room",
            "number_of_toilet",
            "number_of_bed",
            "maximum_guests",
            "address",
            "pet_friendly",
            "house_type",
            "things_to_know",
            "category_id",
            "amenities_id",
            "description",
        )


class RoomListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()  # get_rating 메소드이름 정해져있음! 필요로함!
    photos = TinyPhotoInRoomSerializer(many=True, read_only=True)
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
        model = Room
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
            "rating",
            "owner",
            "number_of_room",
            "number_of_toilet",
            "number_of_bed",
            "maximum_guests",
            "house_type",
        )

    # serializers.SerializerMethodField() 커스텀 하기위해 get_rating만들어야함
    def get_rating(self, room):
        return room.rating()


class RoomDetailSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()  # get_rating 메소드이름 정해져있음! 필요로함!
    cleanliness_rating = serializers.SerializerMethodField()
    accuracy_rating = serializers.SerializerMethodField()
    communication_rating = serializers.SerializerMethodField()
    location_rating = serializers.SerializerMethodField()
    check_in_rating = serializers.SerializerMethodField()
    photos = PhotoInRoomSerializer(many=True, read_only=True)
    category = AddCategorySerializer()
    amenities = AmenitySerializer(many=True)
    is_liked = serializers.SerializerMethodField()
    owner = TinyUserInRoomSerializer()

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
        model = Room
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
            "rating",
            "cleanliness_rating",
            "accuracy_rating",
            "communication_rating",
            "location_rating",
            "check_in_rating",
            "owner",
            "amenities",
            "maximum_guests",
            "cleaning_fee",
            "number_of_room",
            "number_of_toilet",
            "number_of_bed",
            "address",
            "things_to_know",
            "house_type",
            "pet_friendly",
            "city",
            "country",
        )

    # serializers.SerializerMethodField() 커스텀 하기위해 get_rating만들어야함
    def get_rating(self, room):
        return room.rating()

    def get_cleanliness_rating(self, room):
        return room.cleanliness_rating()

    def get_accuracy_rating(self, room):
        return room.accuracy_rating()

    def get_communication_rating(self, room):
        return room.communication_rating()

    def get_location_rating(self, room):
        return room.location_rating()

    def get_check_in_rating(self, room):
        return room.check_in_rating()
