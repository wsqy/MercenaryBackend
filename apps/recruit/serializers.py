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
    # address = AddressShortSerializer()
    class Meta:
        model = PartTimeOrderCard
        fields = ('address', 'start_time', 'end_time', 'enrol_count')
        # read_only_fields = ('id', 'work_time', 'status')


class PartTimeOrderCreateSerializer(serializers.ModelSerializer):
    cards = PartTimeOrderCardSerializer(many=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = PartTimeOrder
        fields = ('user', 'company', 'name', 'description', 'requirement', 'wages', 'settlement_method', 'deposit' ,'cards')

    def create(self, validated_data):
        cards_data = validated_data.pop('cards')
        order = PartTimeOrder.objects.create(**validated_data)
        address_list = []
        for card_data in cards_data:
            PartTimeOrderCard.objects.create(recruit=order, **card_data)
            address_list.append(card_data.get('address').district)
        address_list = list(set(address_list))
        address_info = '多地址可选'
        if len(address_list) == 1:
            address_info = '{}-{}'.format(address_list[0].city.name, address_list[0].name)
        order.address_info=address_info
        order.save()
        return order

    def validate(self, attrs):
        if attrs.get('user').profileextendinfo.admin_company:
            if attrs.get('user').profileextendinfo.admin_company != attrs.get('company'):
                raise serializers.ValidationError('非法请求:企业管理员信息与用户信息不一致')
            else:
                attrs.pop('user')
                return attrs
        else:
            raise serializers.ValidationError('非企业管理员不能创建招募令')


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
        fields = ('id', 'name', 'settlement_method', 'wages', 'cards',)
