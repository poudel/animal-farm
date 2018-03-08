from django.views.generic import (
    DetailView as DetailViewBase,
    ListView as ListViewBase,
    UpdateView as UpdateViewBase,
    CreateView as CreateViewBase,
    DeleteView as DeleteVieBase,
    TemplateView
)


class IndexView(TemplateView):
    template_name = "dashboard.html"


class CreateView(CreateViewBase):
    pass


class ListView(ListViewBase):
    pass


class DetailView(DetailViewBase):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class UpdateView(UpdateViewBase):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class DeleteView(DeleteVieBase):
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
