from rest_framework import serializers

from .models import SubCategory, OrderInfo
from utils.common import generate_order_id


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'template')


class OrderInfoCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs['id'] = generate_order_id(order_type='10')
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderInfoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = '__all__'
