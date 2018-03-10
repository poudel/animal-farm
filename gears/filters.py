from django.db import models

from django_filters.filterset import (
    FILTER_FOR_DBFIELD_DEFAULTS,
    FilterSet as OriginalFilterSet,
)
from django_filters.compat import remote_queryset
from django_filters.filters import ModelChoiceFilter


FILTER_FOR_DBFIELD_DEFAULTS[models.OneToOneField] = {
    'filter_class': ModelChoiceFilter,
    'extra': lambda f: {
        'queryset': remote_queryset(f),
        'to_field_name': "uuid",
    }
}


FILTER_FOR_DBFIELD_DEFAULTS[models.ForeignKey] = {
    'filter_class': ModelChoiceFilter,
    'extra': lambda f: {
        'queryset': remote_queryset(f),
        'to_field_name': "uuid",
    }
}


class FilterSet(OriginalFilterSet):
    FILTER_DEFAULTS = FILTER_FOR_DBFIELD_DEFAULTS
