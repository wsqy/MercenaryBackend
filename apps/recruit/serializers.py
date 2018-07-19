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
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_user(self, user):
        if user.profileextendinfo.admin_company:
            raise serializers.ValidationError('当前用户已认证过企业-{}'.format(user.profileextendinfo.admin_company.name))
        return user

    class Meta:
        model = Company
        exclude = ('weight', 'add_time',)
        read_only_fields = ('status',)
