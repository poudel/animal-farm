from django.contrib import admin
from gears.models import Farm, TxnType, AnimalTxn, AnimalType, Breed, Animal, KbTag, KbArticle


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("tag", "farm", "breed", "gender", "is_sick",)
    search_fields = ("tag", "name", "farm__name",)
    list_filter = ("is_sick", "is_pregnant", "gender", "breed",)


admin.site.register([
    Farm,
    TxnType,
    AnimalTxn,
    AnimalType,
    Breed,
    KbArticle,
    KbTag,
])
