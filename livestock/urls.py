from django.urls import path
from livestock import views


app_name = "livestock"

urlpatterns = [
    path('animal/',
         views.AnimalList.as_view(),
         name="animal-list"
    ),
    path('animal/create/',
         views.AnimalCreate.as_view(),
         name="animal-create"),

    path('animal/<uuid:uuid>/',
         views.AnimalDetail.as_view(),
         name="animal-detail"),

    path('animal/<uuid:uuid>/update/',
         views.AnimalUpdate.as_view(),
         name="animal-update"),

    path('animal/<uuid:uuid>/delete/',
         views.AnimalDelete.as_view(),
         name="animal-delete"),
]
