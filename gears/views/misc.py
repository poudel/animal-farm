from django.views.generic import TemplateView
from django.contrib import messages
from livestock.models import Animal
from gears.models import Farm
from gears.views import UpdateView, DetailView


__all__ = ["DashboardView", "FarmUpdate", "FarmDetail"]


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        # aggrs = Animal.get_for_farm(self.request.farm).active(
            
        # )

        ctx = super().get_context_data(**kwargs)
        return ctx


class FarmDetail(DetailView):
    queryset = Farm.objects.active()
    template_name = "farm_detail.html"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class FarmUpdate(UpdateView):
    """
    This is editable by the owner
    """
    queryset = Farm.objects.active()
    fields = ("name", "address", "contact_mobile",
              "has_breed", "has_herd", "has_weight")
    template_name = "generic_form.html"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Farm information has been updated.")
        return super().get_success_url()
