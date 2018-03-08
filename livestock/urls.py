from django.urls import path
from livestock import views


app_name = "livestock"

urlpatterns = [
    path('animal/', views.AnimalList.as_view(), name="animal-list"),
    path('animal/create/', views.AnimalCreate.as_view(), name="animal-create"),
    path('animal/<int:pk>/', views.AnimalDetail.as_view(), name="animal-detail"),
]
