from rest_framework import serializers

from .models import Company, PartTimeOrder, PartTimeOrderCard, PartTimeOrderSignUp, PartTimeOrderCardSignUp
from area.serializers import AddressShortSerializer
from users.serializers import UserRecruitLiaisonSerializer


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
    class Meta:
        model = PartTimeOrderCard
        fields = ('address', 'start_time', 'end_time', 'enrol_count')


class PartTimeOrderCardInfoSerializer(serializers.ModelSerializer):
    address = AddressShortSerializer()
    class Meta:
        model = PartTimeOrderCard
        fields = ('id', 'address', 'start_time', 'end_time', 'enrol_count')


class PartTimeOrderCardSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartTimeOrderCardSignUp
        fields = ('id', 'status', 'create_time', 'reward')


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
    cards = PartTimeOrderCardInfoSerializer(many=True)
    company = CompanyListSerializer()
    liaison = UserRecruitLiaisonSerializer()
    class Meta:
        model = PartTimeOrder
        fields = '__all__'


class PartTimeOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartTimeOrder
        fields = ('id', 'name', 'settlement_method', 'wages', 'address_info', 'end_time')
        

class PartTimeOrderSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartTimeOrderSignUp
        fields = '__all__'


class PartTimeOrderSignInfoSerializer(serializers.ModelSerializer):
    signs = PartTimeOrderCardSignUpSerializer(many=True)
    recruit =  PartTimeOrderInfoSerializer()

    class Meta:
        model = PartTimeOrderSignUp
        fields = '__all__'


class PartTimeOrderSignListSerializer(serializers.ModelSerializer):
    recruit = PartTimeOrderListSerializer()
    class Meta:
        model = PartTimeOrderSignUp
        fields = '__all__'


class PartTimeOrderSignCreateSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    cards = serializers.ListField(
        child=serializers.IntegerField()
    )
    class Meta:
        model = PartTimeOrderSignUp
        fields = ('user', 'cards', 'recruit')


class PartTimeOrderCardSignCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = PartTimeOrderCardSignUp
        fields = ('user', 'sign', 'recruit', 'card')

    def validate(self, attrs):
        user = attrs.get('user')
        sign = attrs.get('sign')
        recruit = attrs.get('recruit')
        card = attrs.get('card')
        # 检查招募令状态
        if recruit.status < 0:
            raise serializers.ValidationError('所选招募令已取消')

        # 检查报名状态
        if sign.status < 0:
            raise serializers.ValidationError('所选报名已取消')

        # 检查 卡片是否属于 招募令
        if card.recruit != recruit:
            raise serializers.ValidationError('所选卡片不属于属于所选招募令')

        # 检查 报名 对应的招募令是否属于提交的招募令
        if sign.recruit != recruit:
            raise serializers.ValidationError('所选报名不属于属于所选招募令')
        # 检查报名所属的卡片是否属于招募令
        if sign.user != user:
            raise serializers.ValidationError('所选报名非法: 不是本人的报名')
        # 检查是否已报名过此报名
        if PartTimeOrderCardSignUp.objects.filter(user=user, card=card).count():
            raise serializers.ValidationError('不能重复报名卡片')

        return attrs
