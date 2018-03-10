"""
Marketplace is something where farmers can sell their products,
vendors of agriculture equipments etc. will also be able to sell their products
"""
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from gears.models import BaseModel


class Seller(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sellers",
        verbose_name=_("user")
    )
    name = models.CharField(_("name"), max_length=50)
    about = models.TextField(_("about"))
    mobile = models.CharField(_("mobile number"), max_length=10)

    STATUS_CHOICES = [
        ("Pending", _("Pending verification")),
        ("Verified", _("Verified")),
        ("Unverified", _("Unverified")),
        ("Banned", _("Banned")),
        ("Archived", _("Archived"))
    ]
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
        db_index=True
    )

    checker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="checked_sellers",
        verbose_name=_("profile checker")
    )

    class Meta:
        verbose_name = _("seller")
        verbose_name_plural = _("sellers")

    def __str__(self):
        return self.name


class ProductCategory(BaseModel):
    name = models.CharField(_("name"), max_length=50)

    def __str__(self):
        return self.name


class MeasurementUnit(BaseModel):
    name = models.CharField(_("name"), max_length=50)

    def __str__(self):
        return self.name


class Product(BaseModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_products",
        verbose_name=_("created by")
    )
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("seller")
    )
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("category")
    )
    title = models.CharField(_("title"), max_length=100)
    description = models.TextField(_("description"))

    animal = models.ForeignKey(
        "livestock.Animal",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("animal")
    )

    price = models.PositiveIntegerField(_("price"), default=0)

    unit = models.ForeignKey(
        MeasurementUnit,
        on_delete=models.CASCADE,
        verbose_name=_("unit")
    )

    stock_available = models.PositiveIntegerField(
        _("available in stock"),
        default=1,
    )

    tags = TaggableManager()

    def __str__(self):
        return self.title
