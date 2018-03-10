from django.views.generic import TemplateView


__all__ = ["DashboardView"]


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     return ctx
