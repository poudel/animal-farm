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


__all__ = ["AnimalSicknessCreate",]


class AnimalSicknessFormMixin:
    model = AnimalSickness
    # form_class = AnimalSicknessForm
    success_message = "hmm"

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request
        return kw

    def get_success_url(self):
        messages.success(
            self.request,
            self.success_message.format(self=self)
        )
        return reverse_lazy("livestock:animal-detail", args=[self.object.uuid])


class AnimalSicknessCreate(CreateView):
    pass
