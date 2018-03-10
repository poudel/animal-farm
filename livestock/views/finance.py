from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from gears.models import Farm
from gears.views import (
    ListView,
    CreateView,
    DetailView,
    DeleteView,
    UpdateView
)
from livestock.models import AnimalTxn, TxnType
from livestock.forms import AnimalTxnForm
from livestock.filters import AnimalTxnFilterSet


__all__ = [
    "AnimalTxnList", "AnimalTxnCreate",
    "AnimalTxnUpdate",  "AnimalTxnDetail",
    "AnimalTxnDelete",
]


class AnimalTxnMixin:

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('type', 'farm', 'animal').filter(
            Q(farm__owner=self.request.user) |
            Q(animal__farm__owner=self.request.user)
        ).order_by("-id")


class AnimalTxnList(AnimalTxnMixin, ListView):
    model = AnimalTxn
    filterset_class = AnimalTxnFilterSet


class TxnFormMixin:
    model = AnimalTxn
    template_name = "generic_form.html"
    form_class = AnimalTxnForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request
        return kw


class AnimalTxnCreate(TxnFormMixin, CreateView):

    def get_success_url(self):
        messages.success(self.request, "Successfully added transaction")
        return reverse_lazy("livestock:txn-detail", args=[self.object.uuid])


class AnimalTxnUpdate(TxnFormMixin, UpdateView):
    pass


class AnimalTxnDetail(AnimalTxnMixin, DetailView):
    model = AnimalTxn


class AnimalTxnDelete(AnimalTxnMixin, DetailView):
    success_url = reverse_lazy("livestock:txn-list")
    hard_delete = True
