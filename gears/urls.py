from django.urls import path
from rest_framework import routers
from gears import api, views


urlpatterns = [
    path('animal/', views.AnimalList.as_view(), name="animal-list"),
    path('animal/create/', views.AnimalCreate.as_view(), name="animal-create"),
    path('animal/<int:pk>/', views.AnimalDetail.as_view(), name="animal-detail"),
]


# router = routers.SimpleRouter()

# router.register("api/breed", api.BreedAPI)

# router.register("api/animaltype", api.AnimalTypeAPI)

# router.register("api/txntype", api.TxnTypeAPI)

# router.register("api/farm", api.FarmAPI)

# router.register("api/animal", api.AnimalAPI)

# router.register("api/basic", api.BasicAPI, base_name="basic")

