from django.urls import path
from gears import views

app_name = "gears"

urlpatterns = [
    path("farm/<uuid:uuid>/", views.FarmDetail.as_view(), name="farm-detail"),
    path("farm/<uuid:uuid>/update/", views.FarmUpdate.as_view(), name="farm-update")
]
