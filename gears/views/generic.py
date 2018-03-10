from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.contrib import messages
from django.views.generic import (
    DetailView as DetailViewBase,
    ListView as ListViewBase,
    UpdateView as UpdateViewBase,
    CreateView as CreateViewBase,
    DeleteView as DeleteViewBase,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django_filters.views import FilterMixin


__all__ = ["CreateView", "ListView", "DetailView", "UpdateView", "DeleteView"]


class CreateView(LoginRequiredMixin, CreateViewBase):
    pass


class ListView(LoginRequiredMixin, FilterMixin, ListViewBase):
    paginate_by = 50
    filter_fields = None

    def get(self, request, *args, **kwargs):

        if self.filterset_class or self.filter_fields:
            filterset_class = self.get_filterset_class()
            self.filterset = self.get_filterset(filterset_class)

            self.object_list = self.filterset.qs
            context = self.get_context_data(filter=self.filterset,
                                        object_list=self.object_list)
            return self.render_to_response(context)
        return super().get(request, *args, **kwargs)


class DetailView(LoginRequiredMixin, DetailViewBase):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class UpdateView(LoginRequiredMixin, UpdateViewBase):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class DeleteView(LoginRequiredMixin, DeleteViewBase):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    hard_delete = False
    message = "{self.object} has been deleted."
    detail_url_name = None

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete(hard_delete=self.hard_delete)
        return redirect(success_url)

    def get_success_url(self):
        messages.error(
            self.request,
            self.message.format(self=self)
        )
        return super().get_success_url()

    def get_cancel_url(self):
        return reverse(self.detail_url_name, args=[self.object.uuid])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cancel_url'] = self.get_cancel_url()
        return ctx
