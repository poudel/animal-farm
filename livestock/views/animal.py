from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from gears.views import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView
)
from livestock.models import Animal, Herd
from livestock.forms import AnimalForm


__all__ = [
    "AnimalCreate",
    "AnimalList",
    "AnimalDetail",
    "AnimalUpdate",
    "AnimalDelete",
    "HerdList",
    "HerdCreate",
    "HerdUpdate",
    "HerdDelete"
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


class HerdMixin:
    queryset = Herd.objects.active()

    def get_queryset(self):
        return self.queryset.filter(
            farm__owner=self.request.user
        ).order_by('-id')


class HerdList(HerdMixin, ListView):
    pass


class HerdFormMixin:
    model = Herd
    fields = ("name",)
    success_message = "Successfully saved {self.object.name}"
    template_name = "generic_form.html"

    def get_success_url(self):
        messages.success(
            self.request,
            self.success_message.format(self=self)
        )
        return reverse_lazy("livestock:herd-list")

    def form_valid(self, form):
        if not hasattr(form.instance, 'farm'):
            form.instance.farm = self.request.farm
        return super().form_valid(form)


class HerdCreate(HerdFormMixin, CreateView):
    pass


class HerdUpdate(HerdFormMixin, UpdateView):
    pass


class HerdDelete(HerdMixin, DeleteView):
    template_name = "generic_delete_confirm.html"
    success_url = reverse_lazy("livestock:herd-list")
    message = "Herd {self.object.herd} has been deleted."

    def get_cancel_url(self):
        return reverse_lazy("livestock:herd-list")
