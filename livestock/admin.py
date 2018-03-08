from django.contrib import admin

from livestock.models import (
    IdentityType,
    AnimalType,
    Breed,
    Herd,
    Animal,
    AnimalEventType,
    AnimalEvent,
    SicknessType,
    AnimalSickness,
    TxnType,
    AnimalTxn,
    MedicationType,
    AnimalMedication
)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("identity", "farm", "breed", "gender", "is_sick",)
    search_fields = ("identifier", "name", "farm__name",)
    list_filter = ("is_sick", "is_pregnant", "gender", "breed",)


admin.site.register([
    IdentityType,
    AnimalType,
    Breed,
    Herd,
    AnimalEventType,
    AnimalEvent,
    SicknessType,
    AnimalSickness,
    TxnType,
    AnimalTxn,
    MedicationType,
    AnimalMedication
])
