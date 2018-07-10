from rest_framework import serializers

from .models import Company
from area.serializers import AddressShortSerializer


class CompanyListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Company
        exclude = ('introduce', 'address')


class CompanyInfoSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    address = AddressShortSerializer()
    class Meta:
        model = Company
        fields = '__all__'
