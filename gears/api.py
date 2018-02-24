from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from gears.models import AnimalType, TxnType, Farm, Breed, AnimalTxn, Animal
from gears.serialiizers import (
    AnimalTypeSerializer,
    TxnTypeSerializer,
    FarmSerializer,
    BreedSerializer,
    AnimalSerializer,
    AnimalTxnSerializer
)


class BaseAPI:
    permission_classes = (IsAuthenticated,)


class BasicAPI(BaseAPI, ViewSet):

    @list_route(methods=["get"])
    def info(self, request):
        if not request.user.is_authenticated:
            return Response({})

        # TODO use serializers
        u = request.user
        data = {
            "id": u.id,
            "name": u.first_name + u.last_name,
            "token": u.auth_token.key
        }
        return Response(data)


class TxnTypeAPI(BaseAPI, ReadOnlyModelViewSet):
    queryset = TxnType.objects.all()
    serializer_class=  TxnTypeSerializer


class AnimalTypeAPI(BaseAPI, ReadOnlyModelViewSet):
    queryset = AnimalType.objects.all()
    serializer_class = AnimalTypeSerializer


class BreedAPI(BaseAPI, ReadOnlyModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class FarmAPI(BaseAPI, ReadOnlyModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class AnimalAPI(BaseAPI, ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            farm__owner=self.request.user
        ).order_by('-id')


class AnimalTxnAPI(BaseAPI, ModelViewSet):
    queryset = AnimalTxn.objects.all()
    serializer_class = AnimalTxnSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            animal__farm__owner=self.request.user
        )
