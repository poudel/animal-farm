from django import forms
from livestock.models import Animal, IdentityType


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
            'is_pregnant',
            'due_date',
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
                animal = Animal.objects.get(
                    identity_type=identity_type,
                    identifier__iexact=identifier,
                    farm=self.request.farm
                )
            except Animal.DoesNotExist:
                pass
            else:
                self.add_error(
                    "identifier",
                    "A cattle identified as '{}' already exists."
                    .format(animal.identity)
                )
        return cd
