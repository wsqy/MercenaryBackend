import django_filters

from .models import District

class DistrictFilter(django_filters.rest_framework.FilterSet):
    city_name = django_filters.Filter(field_name='city', lookup_expr='name', help_text='市(名称)', label='市(名称)')

    class Meta:
        model = District
        fields = ['city', 'city_name']
