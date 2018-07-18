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


class CompanyCreateSerializer(serializers.ModelSerializer):
    remark = serializers.CharField(label='申请备注', help_text='申请备注',)
    class Meta:
        model = Company
        exclude = ('weight', 'add_time',)
        read_only_fields = ('status',)
