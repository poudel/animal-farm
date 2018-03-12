from django.contrib import messages
from django.urls import reverse_lazy
from gears.views import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from livestock.models import (
    AnimalSickness,
    SicknessType,
    AnimalMedication,
    MedicationType
)
from livestock.forms import AnimalSicknessForm


__all__ = [
    "AnimalSicknessCreate",
    "AnimalSicknessUpdate",
    "AnimalSicknessDetail",
    "AnimalSicknessList",
]


class AnimalSicknessFormMixin:
    model = AnimalSickness
    form_class = AnimalSicknessForm
    template_name = "generic_form.html"
    success_message = "Successfully saved sickness information."

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request
        return kw

    def get_success_url(self):
        messages.success(
            self.request,
            self.success_message.format(self=self)
        )
        return reverse_lazy("livestock:animal-list")


class AnimalSicknessCreate(AnimalSicknessFormMixin, CreateView):
    pass


class AnimalSicknessUpdate(AnimalSicknessFormMixin, UpdateView):
    pass


class AnimalSicknessDetail(DetailView):
    pass


class AnimalSicknessList(ListView):
    pass
