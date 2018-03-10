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
    model = AnimalTxn
    queryset = AnimalTxn.objects.active()

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
    success_message = "mmm"

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw['request'] = self.request
        return kw

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse_lazy("livestock:txn-detail", args=[self.object.uuid])


class AnimalTxnCreate(TxnFormMixin, CreateView):
    success_message = "Successfully added transaction."


class AnimalTxnUpdate(TxnFormMixin, UpdateView):
    success_message = "Successfully updated transaction."


class AnimalTxnDetail(AnimalTxnMixin, DetailView):
    pass


class AnimalTxnDelete(AnimalTxnMixin, DeleteView):
    success_url = reverse_lazy("livestock:txn-list")
    hard_delete = False
    template_name = "generic_delete_confirm.html"
    detail_url_name = "livestock:txn-detail"
