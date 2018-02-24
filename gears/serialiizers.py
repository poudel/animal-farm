from rest_framework import serializers
from gears.models import (
    Farm,
    AnimalType,
    Breed,
    TxnType,
    Animal,
    AnimalTxn,
    KbArticle,
    KbTag,
)


class KbTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = KbTag
        fields = ('tag',)


class KbArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = KbArticle
        fields = ('title', 'slug', 'content', 'tags', 'author')
        extra_kwargs = {
            'author': {'read_only': True}
        }


class AnimalTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnimalType
        fields = ("id", "name")


class BreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Breed
        fields = ("id", "animal_type", "name", "breeding_ages")


class TxnTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TxnType
        fields = ('id', 'name', 'is_expense')


class FarmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Farm
        fields = ("id", "owner", "name", "address")


class AnimalSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    money = serializers.SerializerMethodField()

    def get_avatar(self, animal):
        return "https://via.placeholder.com/60x60"

    def get_money(self, animal):
        # Return information about expenses and earnings
        # for the past month
        return {"expenses": 0, "earnings": 0, "statement": animal.id}

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data["farm"] = Farm.objects.get(owner=user)
        return super().create(validated_data)

    class Meta:
        model = Animal
        fields = (
            "id", "parent",
            "farm",
            "name",
            "tag",
            "breed",
            "dob_bs",
            "dob",
            "milk_morning",
            "milk_day",
            "milk_evening",
            "avatar",
            "money"
        )
        ro = {"read_only": True}
        extra_kwargs = {
            "parent": ro,
            "farm": ro,
            "dob": ro,
        }


class AnimalTxnSerializer(serializers.ModelSerializer):

    def validate_animal(self, value):
        user = self.context["request"].user
        qs = Animal.objects.filter(
            farm__in=user.farm_set.all(),
            id=value.id
        )
        if not qs.exists():
            raise serializers.ValidationError("No such animal found.")
        return value

    class Meta:
        model = AnimalTxn
        fields = ("id", "animal", "txn_type", "amount", "remarks")
