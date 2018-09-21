import django_filters

from .models import PartTimeOrder


class PartTimeOrderFilter(django_filters.rest_framework.FilterSet):
    """
    兼职招募令的 过滤类
    """
    district = django_filters.Filter(field_name='cards', lookup_expr='address__district__name', help_text='县/区', label='县/区')
    city = django_filters.Filter(field_name='cards', lookup_expr='address__district__city__name', help_text='市', label='市')

    class Meta:
        model = PartTimeOrder
        fields = ['city', 'district', 'settlement_method', 'company']
