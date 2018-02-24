from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from gears.models import Animal
from gears.forms import AnimalForm


class IndexView(TemplateView):
    template_name = "dashboard.html"


class AnimalCreate(CreateView):
    model = Animal
    form_class = AnimalForm

    def form_valid(self, form):
        form.instance.farm = self.request.user.farm_set.get()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("animal-detail", args=[self.object.id])


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
