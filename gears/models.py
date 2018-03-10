import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class DefaultQuerySet(models.QuerySet):

    def active(self, *args, **kwargs):
        return self.filter(is_deleted=False).filter(*args, **kwargs)


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(
        _("is deleted"),
        default=False,
        help_text=_("Set this to True to soft-delete")
    )

    objects = DefaultQuerySet.as_manager()

    class Meta:
        abstract = True

    def delete(self, hard_delete=False):
        if hard_delete:
            super().delete()
        else:
            self.is_deleted = True
            self.save()
        return self


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

    has_breed = models.BooleanField(_("has breed"), default=True)
    has_herd = models.BooleanField(_("has herd"), default=True)
    has_weight = models.BooleanField(_("has weight"), default=True)
    has_dairy_cattle = models.BooleanField(_("has dairy cattle"), default=True)

    class Meta:
        verbose_name = _("farm")
        verbose_name_plural = _("farms")

    def __str__(self):
        return self.name or str(self.owner)
