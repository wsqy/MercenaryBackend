import django_filters

from .models import OrderInfo


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class OrderFilter(django_filters.rest_framework.FilterSet):
    """
    订单的过滤类
    """
    status__in = NumberInFilter(name='status', lookup_expr='in', help_text='订单状态范围')
    # classification = django_filters.NumberFilter(name='category__classification', help_text='一级分类')
    category = django_filters.NumberFilter(name='category', help_text='所属分类')
    school = django_filters.NumberFilter(name='school', help_text='学校')

    class Meta:
        model = OrderInfo
        # fields = ['deposit', 'status__in', 'classification']
        fields = ['deposit', 'status__in', 'category']
