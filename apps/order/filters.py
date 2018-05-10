import django_filters

from .models import OrderInfo


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class OrderFilter(django_filters.rest_framework.FilterSet):
    """
    订单的过滤类
    """
    status__in = NumberInFilter(name='status', lookup_expr='in', help_text='订单状态范围')
    classification = django_filters.NumberFilter(name='category__classification',
                                                 help_text='一级分类')

    class Meta:
        model = OrderInfo
        fields = ['deposit', 'status__in', 'classification']
