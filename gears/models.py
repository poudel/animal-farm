import uuid
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class DefaultQuerySet(models.QuerySet):

    def active(self, *args, **kwargs):
        return self.filter(is_deleted=False).filter(*args, **kwargs)


class DefaultManager(models.Manager):

    def get_queryset(self):
        return DefaultQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        return self.get_queryset().active(*args, **kwargs)


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(
        _("is deleted"),
        default=False,
        help_text=_("Set this to True to soft-delete")
    )

    objects = DefaultManager()

    class Meta:
        abstract = True

    def delete(self, hard_delete=False):
        if hard_delete:
            super().delete()
        else:
            self.is_deleted = True
            self.save()
        return self


class FarmManager(DefaultManager):

    def create_default(self, user):
        farm, _ = self.get_or_create(
            owner=user,
            name="FarmHouse",
        )
        return farm


class Farm(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("owner"),
        related_name="farms",
        on_delete=models.PROTECT
    )
    name = models.CharField(_("name"), max_length=100, blank=True)
    address = models.CharField(_("address"), max_length=100, blank=True)
    contact_mobile = models.CharField(_("contact mobile"), max_length=10, blank=True)

    default_identity_type = models.ForeignKey(
        "livestock.IdentityType",
        verbose_name=_("default identity type"),
        on_delete=models.SET_NULL,
        null=True
    )

    has_breed = models.BooleanField(
        _("show breed field"),
        default=True,
        help_text=_("If enabled, will show breed field while adding/updating animals.")
    )
    has_herd = models.BooleanField(
        _("show herd field"),
        default=False,
        help_text=_("If enabled, will show herd field while adding/updating animals.")
    )
    has_weight = models.BooleanField(
        _("show weight field"),
        default=False,
        help_text=_("If enabled, will show weight field while adding/updating animals.")
    )
    has_dairy_cattle = models.BooleanField(_("has dairy cattle"), default=True)

    objects = FarmManager()

    class Meta:
        verbose_name = _("farm")
        verbose_name_plural = _("farms")

    def __str__(self):
        return self.name or str(self.owner)

    def get_absolute_url(self):
        return reverse("gears:farm-detail", args=[self.uuid])
