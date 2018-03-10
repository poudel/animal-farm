from datetime import date
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from gears.models import BaseModel, Farm


class IdentityType(BaseModel):
    name = models.CharField(_("name"), max_length=20, unique=True)

    def __str__(self):
        return self.name


class AnimalType(BaseModel):
    name = models.CharField(_("name"), max_length=100, unique=True)

    def __str__(self):
        return self.name


class Breed(BaseModel):
    animal_type = models.ForeignKey(
        AnimalType,
        verbose_name=_("animal type"),
        on_delete=models.PROTECT
    )
    name = models.CharField(_("name"), max_length=200, unique=True)
    breeding_ages = models.CharField(_("breeding ages"), max_length=200, blank=True)

    def __str__(self):
        return f"{self.name} - {self.animal_type}"


class Herd(BaseModel):
    name = models.CharField(_("name"), max_length=50, unique=True)

    def __str__(self):
        return self.name


class Animal(BaseModel):
    parent = models.ForeignKey(
        'self',
        verbose_name=_("parent"),
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    farm = models.ForeignKey(
        Farm,
        verbose_name=_("farm"),
        on_delete=models.CASCADE
    )

    identity_type = models.ForeignKey(
        IdentityType,
        verbose_name=_("identity type"),
        on_delete=models.CASCADE
    )
    identifier = models.CharField(_("identifier"), max_length=100)

    herd = models.ForeignKey(
        Herd,
        verbose_name=_("herd"),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    breed = models.ForeignKey(
        Breed,
        verbose_name=_("breed"),
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    dob = models.DateField(_("date of birth (AD)"), null=True, blank=True)

    GENDER_CHOICES = [
        ("Female", _("Female")),
        ("Male", _("Male"))
    ]

    gender = models.CharField(
        _("gender"),
        max_length=10,
        choices=GENDER_CHOICES,
        default="Female"
    )

    is_pregnant = models.BooleanField(_("is pregnant"), default=False)
    due_date = models.DateField(_("due date"), null=True, blank=True)

    lactation = models.CharField(
        _("lactation"),
        max_length=20,
        choices=[
            ("Never", _("Never")),
            ("Lactating", _("Lactating")),
            ("Stopped", _("Stopped"))
        ],
        default="Never"
    )

    milk_day = models.FloatField(
        _("milk per day (in litres)"),
        null=True,
        blank=True
    )

    is_sick = models.BooleanField(_("is sick"), default=False)
    weight = models.FloatField(_("weight"), null=True, blank=True)

    class Meta:
        unique_together = [('farm', 'identity_type', 'identifier')]
        verbose_name = _("animal")
        verbose_name_plural = _("animals")

    def __str__(self):
        return f"{self.farm}; {self.identity};"

    @property
    def identity(self):
        return "{}-{}".format(self.identity_type, self.identifier)

    @property
    def age(self):
        if self.dob:
            return (date.today() - self.dob)

    @property
    def is_female(self):
        return self.gender == "Female"

    @property
    def is_male(self):
        return not self.is_female


class TxnType(BaseModel):
    name = models.CharField(_("name"), max_length=200)
    is_expense = models.BooleanField(_("is expense"), default=False)

    class Meta:
        unique_together = [('name', 'is_expense')]
        verbose_name = _("transaction type")
        verbose_name_plural = _("transaction types")

    def __str__(self):
        return self.name


class AnimalTxn(BaseModel):
    farm = models.ForeignKey(
        Farm,
        verbose_name=_("farm"),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    animal = models.ForeignKey(
        Animal,
        verbose_name=_("animal"),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    type = models.ForeignKey(
        TxnType,
        verbose_name=_("transaction type"),
        on_delete=models.PROTECT
    )
    amount = models.FloatField(_("amount"))
    remarks = models.CharField(_("remarks"), max_length=200, blank=True)

    class Meta:
        verbose_name = _("animal transaction")
        verbose_name_plural = _("animal transactions")

    def __str__(self):
        return f"{self.animal} - {self.type} - {self.amount}"

    @property
    def owner(self):
        return self.animal or self.farm


class AnimalEventType(BaseModel):
    name = models.CharField(_("name"), max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("animal event type")
        verbose_name_plural = _("animal sickness types")


class AnimalEvent(BaseModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("created by"),
        on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        AnimalEventType,
        verbose_name=_("event type"),
        on_delete=models.CASCADE,
        related_name="events"
    )
    animal = models.ForeignKey(
        Animal,
        verbose_name=_("animal"),
        on_delete=models.CASCADE,
        related_name="events"
    )
    description = models.TextField(_("description"))

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("animal event")
        verbose_name_plural = _("animal events")


class SicknessType(BaseModel):
    name = models.CharField(_("name"), max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("sickness type")
        verbose_name_plural = _("sicknes types")


class AnimalSickness(BaseModel):
    animal = models.ForeignKey(
        Animal,
        verbose_name=_("animal"),
        on_delete=models.CASCADE
    )
    description = models.CharField(_("description"), max_length=200)
    is_recovered = models.BooleanField(_("is recovered"), default=False)
    recovered_on = models.DateField(_("recovered on"), null=True, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("animal sickness")
        verbose_name_plural = _("animal sickness")


class MedicationType(BaseModel):
    name = models.CharField(_("name"), max_length=50, unique=True)
    description = models.CharField(_("description"), max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("medication type")
        verbose_name_plural = _("medication types")


class AnimalMedication(BaseModel):
    type = models.ForeignKey(
        MedicationType,
        verbose_name=_("medication type"),
        on_delete=models.CASCADE
    )
    animal = models.ForeignKey(
        Animal,
        verbose_name=_("animal"),
        on_delete=models.CASCADE
    )
    name = models.CharField(_("name"), max_length=100)
    txn = models.ForeignKey(
        AnimalTxn,
        verbose_name=_("transaction"),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("animal medication")
        verbose_name_plural = _("animal medications")
