from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from livestock.models import Animal
from livestock.forms import AnimalForm
from gears.views import (
    CreateView,
    ListView,
    UpdateView,
    DetailView
)


class AnimalCreate(CreateView):
    model = Animal
    form_class = AnimalForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request
        return kw

    def get_success_url(self):
        return reverse_lazy("livestock:animal-detail", args=[self.object.id])


class AnimalList(LoginRequiredMixin, ListView):
    model = Animal
    
    def get_queryset(self):
        return super().get_queryset().filter(
            farm__owner=self.request.user
        ).order_by('-id')


class AnimalDetail(DetailView):
    model = Animal

    def get_queryset(self):
        return super().get_queryset().filter(farm__owner=self.request.user)


class AnimalUpdate(UpdateView):
    pass
