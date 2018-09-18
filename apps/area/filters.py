import django_filters

from .models import District, City


class CityFilter(django_filters.rest_framework.FilterSet):
    province_name = django_filters.Filter(field_name='province', lookup_expr='name__icontains', help_text='省(名称)', label='省(名称)')

    class Meta:
        model = City
        fields = ['id', 'name', 'province', 'province_name']


class DistrictFilter(django_filters.rest_framework.FilterSet):
    city_name = django_filters.Filter(field_name='city', lookup_expr='name__icontains', help_text='市(名称)', label='市(名称)')

    class Meta:
        model = District
        fields = ['city', 'city_name']
