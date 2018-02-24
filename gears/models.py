from datetime import date
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Farm(BaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name or str(self.owner)


class AnimalType(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Breed(BaseModel):
    animal_type = models.ForeignKey(AnimalType, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, unique=True)
    breeding_ages = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.name} - {self.animal_type}"


class Animal(BaseModel):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    tag = models.CharField(_("tag"), max_length=100)
    name = models.CharField(_("name"), max_length=100, blank=True)
    breed = models.ForeignKey(
        Breed,
        verbose_name=_("breed"),
        null=True,
        on_delete=models.PROTECT
    )
    dob_bs = models.CharField(_("date of birth (BS)"),
                              max_length=15, blank=True, null=True)
    dob = models.DateField(_("date of birth (AD)"), null=True, blank=True)

    gender = models.CharField(
        _("gender"),
        max_length=10,
        choices=[
            ("Female", _("Female")),
            ("Male", _("Male")),
        ],
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

    class Meta:
        unique_together = [('farm', 'tag')]

    def __str__(self):
        return f"{self.farm} - {self.tag} - {self.name}"

    @property
    def age(self):
        if self.dob:
            return (date.today() - self.dob).days

    @property
    def is_female(self):
        return self.gender == "Female"

    @property
    def is_male(self):
        return not self.is_female


class AnimalEventType(BaseModel):
    name = models.CharField(_("name"), max_length=50, unique=True)
    name_np = models.CharField(_("name np"), max_length=50)

    def __str__(self):
        return self.name


class AnimalEvent(BaseModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        AnimalEventType,
        on_delete=models.CASCADE,
        related_name="events"
    )
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="events"
    )
    description = models.TextField(_("description"))

    def __str__(self):
        return self.description


class SicknessType(BaseModel):
    name = models.CharField(_("name"), max_length=100, unique=True)
    name_np = models.CharField(_("name np"), max_length=100)

    def __str__(self):
        return self.name


class AnimalSickness(BaseModel):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    description = models.CharField(_("description"), max_length=200)
    is_recovered = models.BooleanField(_("is recovered"), default=False)
    recovered_on = models.DateField(_("recovered on"), null=True, blank=True)

    def __str__(self):
        return self.description


class TxnType(BaseModel):
    name = models.CharField(max_length=200)
    name_np = models.CharField(max_length=200, blank=True)
    is_expense = models.BooleanField(default=False)

    class Meta:
        unique_together = [('name', 'is_expense')]

    def __str__(self):
        return self.name


class AnimalTxn(BaseModel):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    type = models.ForeignKey(TxnType, on_delete=models.PROTECT)
    amount = models.FloatField()
    remarks = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.animal} - {self.type} - {self.amount}"


class MedicineType(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    name_np = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Medicine(BaseModel):
    type = models.ForeignKey(MedicineType, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    txn = models.ForeignKey(AnimalTxn, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class KbTag(BaseModel):
    slug = models.SlugField()

    def __str__(self):
        return self.slug


class KbArticle(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField(blank=True)
    tags = models.ManyToManyField(KbTag, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.title
