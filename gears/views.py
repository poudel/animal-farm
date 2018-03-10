from django.core.exceptions import ImproperlyConfigured
from django.views.generic import (
    DetailView as DetailViewBase,
    ListView as ListViewBase,
    UpdateView as UpdateViewBase,
    CreateView as CreateViewBase,
    DeleteView as DeleteVieBase,
    TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


__all__ = ["IndexView", "CreateView", "ListView", "DetailView", "UpdateView", "DeleteView"]


class IndexView(TemplateView):
    template_name = "dashboard.html"


class CreateView(LoginRequiredMixin, CreateViewBase):
    pass


class ListView(LoginRequiredMixin, ListViewBase):
    pass


class DetailView(LoginRequiredMixin, DetailViewBase):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class UpdateView(LoginRequiredMixin, UpdateViewBase):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class DeleteView(LoginRequiredMixin, DeleteVieBase):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
    hard_delete = False

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        if self.hard_delete:
            self.object.delete()
        else:
            if not hasattr(self.object, "is_deleted"):
                raise ImproperlyConfigured(
                    "The model instance must have "
                    "is_deleted field for a soft deletion."
                )
        return redirect(success_url)
