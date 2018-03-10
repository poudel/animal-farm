import django_filters
from gears.filters import FilterSet
from livestock.models import AnimalTxn


class AnimalTxnFilterSet(FilterSet):

    class Meta:
        model = AnimalTxn
        fields = ("animal", "farm", "created_by", "type", "type__is_expense")
