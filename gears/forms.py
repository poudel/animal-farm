from django import forms
from gears.models import Animal


class AnimalForm(forms.ModelForm):

    class Meta:
        model = Animal
        fields = [
            'tag',
            'breed',
            'dob',
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
