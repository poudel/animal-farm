from django.contrib import admin
from gears.models import Farm


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_mobile", "address")
    search_fields = ("name", "contact_mobile", "address",)
    readonly_fields = ("uuid",)
