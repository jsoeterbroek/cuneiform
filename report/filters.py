from django import forms
from signoff.models import PrescriptionEvent
import django_filters


class PeFilter(django_filters.FilterSet):
    pe = django_filters.CharFilter(lookup_expr='icontains')
    tobe_administered_period = django_filters.CharFilter(lookup_expr='icontains')
    tobe_administered_date = django_filters.NumberFilter(field_name='tobe_administered_date', lookup_expr='day')

    class Meta:
        model = PrescriptionEvent
        fields = [
            'prescription',
            'tobe_administered_date',
            'tobe_administered_period',
            'tobe_administered_who',
            'tobe_administered_what',
            'tobe_administered_howmuch',
  
        ]


class PeFilterSignoff(django_filters.FilterSet):
    pe = django_filters.CharFilter(lookup_expr='icontains')
    is_signedoff = django_filters.BooleanFilter()
    is_signedoff_when = django_filters.DateTimeFilter()

    class Meta:
        model = PrescriptionEvent
        fields = [
            'prescription',
            'tobe_administered_date',
            'tobe_administered_period',
            'tobe_administered_who',
            'is_signedoff',
            'is_signedoff_who',
            'is_signedoff_when',
        ]


