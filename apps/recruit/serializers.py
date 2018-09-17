from rest_framework import serializers

from .models import Company, PartTimeOrder, PartTimeOrderCard
from area.serializers import AddressShortSerializer
from users.serializers import UserOrderListSerializer


class CompanyListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Company
        exclude = ('introduce', 'address')


class CompanyInfoSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='get_status_display')
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
        fields = ('name', 'user', 'telephone', 'address', 'logo')


class PartTimeOrderCardSerializer(serializers.ModelSerializer):
    address = AddressShortSerializer()
    class Meta:
        model = PartTimeOrderCard
        fields = '__all__'
        read_only_fields = ('id', 'work_time', 'status')


class PartTimeOrderCreateSerializer(serializers.ModelSerializer):
    cards = PartTimeOrderCardSerializer(many=True)
    class Meta:
        model = PartTimeOrder
        fields = ('name', 'company', 'description', 'requirement', 'wages', 'settlement_method', 'deposit' ,'cards')


class PartTimeOrderInfoSerializer(serializers.ModelSerializer):
    cards = PartTimeOrderCardSerializer(many=True)
    company = CompanyListSerializer()
    liaison = UserOrderListSerializer()
    class Meta:
        model = PartTimeOrder
        fields = '__all__'


class PartTimeOrderListSerializer(serializers.ModelSerializer):
    cards = PartTimeOrderCardSerializer(many=True)
    class Meta:
        model = PartTimeOrder
        fields = ('id', 'name', 'cards',)
