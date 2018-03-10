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

    # finance
    path('transaction/',
         views.AnimalTxnList.as_view(),
         name="txn-list"),

    path('transaction/create/',
         views.AnimalTxnCreate.as_view(),
         name="txn-create"),

    path('transaction/<uuid:uuid>/',
         views.AnimalTxnDetail.as_view(),
         name="txn-detail"),

    path('transaction/<uuid:uuid>/update/',
         views.AnimalTxnUpdate.as_view(),
         name="txn-update"),

    path('transaction/<uuid:uuid>/delete/',
         views.AnimalTxnDelete.as_view(),
         name="txn-delete"),

]
