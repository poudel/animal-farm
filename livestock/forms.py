from django import forms
from django.utils.translation import ugettext_lazy as _
from livestock.models import Animal, IdentityType, AnimalTxn, TxnType


class AnimalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        conditional_fields = [
            ('has_breed', 'breed'),
            ('has_herd', 'herd'),
            ('has_weight', 'weight'),
            ('has_dairy_cattle', 'lactation'),
            ('has_dairy_cattle', 'milk_day'),
        ]

        for has_field, field in conditional_fields:
            if not getattr(self.request.farm, has_field):
                del self.fields[field]

    class Meta:
        model = Animal
        fields = [
            'identity_type',
            'identifier',
            'breed',
            'herd',
            'dob',
            'weight',
            'gender',
            'lactation',
            'milk_day'
        ]
        widgets = {
            "gender": forms.RadioSelect(),
            "lactation": forms.RadioSelect(),
        }

    def save(self, *args, **kwargs):
        self.instance.farm = self.request.farm
        return super().save(*args, **kwargs)

    def clean(self):
        cd = super().clean()

        identity_type, identifier = cd.get('identity_type'), cd.get('identifier')

        if identity_type and identifier:
            try:
                queryset = Animal.objects.filter(
                    identity_type=identity_type,
                    identifier__iexact=identifier,
                    farm=self.request.farm
                )
                if self.instance:
                    queryset = queryset.exclude(id=self.instance.id)

                animal = queryset.get()
            except Animal.DoesNotExist:
                pass
            else:
                self.add_error(
                    "identifier",
                    "The identifier '{}' is not available for registration."
                    .format(animal.identity)
                )
        return cd


class AnimalTxnForm(forms.ModelForm):

    class Meta:
        model = AnimalTxn
        fields = ("animal", "type", "amount", "remarks")
        help_texts = {
            "animal": _("Specify an animal if this transaction is specific to it.")
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields['animal'].queryset = Animal.get_for_farm(self.request.farm)

    def save(self, *args, **kwargs):
        self.instance.farm = self.request.farm
        self.instance.created_by = self.request.user
        return super().save(*args, **kwargs)
