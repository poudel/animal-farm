from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from livestock.models import Animal
from livestock.forms import AnimalForm
from gears.views import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView
)


__all__ = [
    "AnimalCreate",
    "AnimalList",
    "AnimalDetail",
    "AnimalUpdate",
    "AnimalDelete"
]


class AnimalFormMixin:
    model = Animal
    form_class = AnimalForm
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


class AnimalCreate(AnimalFormMixin, CreateView):
    success_message = "Animal {self.object.identity} has been created."


class AnimalList(ListView):
    queryset = Animal.objects.active()

    def get_queryset(self):
        return self.queryset.filter(farm__owner=self.request.user).order_by('-id')


class AnimalDetailMixin:
    queryset = Animal.objects.active()

    def get_queryset(self):
        return self.queryset.filter(farm__owner=self.request.user)


class AnimalDetail(AnimalDetailMixin, DetailView):
    pass


class AnimalUpdate(AnimalDetailMixin, AnimalFormMixin, UpdateView):
    success_message = "Animal {self.object.identity} has been updated."


class AnimalDelete(AnimalDetailMixin, DeleteView):
    template_name = "generic_delete_confirm.html"
    success_url = reverse_lazy("livestock:animal-list")
    message = "{self.object.identity} has been deleted."
    detail_url_name = "livestock:animal-detail"
