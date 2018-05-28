from rest_framework import serializers

from .models import BalanceDetail, BankCard, WithDraw
from users.models import ProfileExtendInfo


class BalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileExtendInfo
        fields = ('balance', 'deposit_freeze')
        read_only_fields = ('balance', 'deposit_freeze')


class BalanceListSerializer(serializers.ModelSerializer):
    origin_type = serializers.CharField(source='get_origin_type_display')

    class Meta:
        model = BalanceDetail
        fields = ('origin_type', 'order', 'balance', 'remark', 'add_time')


class BankCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankCard
        fields = ('id', 'user', 'card_no', 'card_type', 'is_credit', 'bank')


class WithDrawCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    balance = serializers.IntegerField(required=True, label='提现金额',
                                       min_value=1, help_text='提现金额',
                                       error_messages={
                                           'min_value': '提现金额不能小于0',
                                           'blank': '请输入提现金额',
                                           'required': '请输入提现金额',
                                       })

    def validate(self, attrs):
        balance = attrs.get('balance')
        try:
            user = ProfileExtendInfo.objects.get(user_id=attrs.get('user').id)
        except Exception as e:
            raise serializers.ValidationError('请求身份异常,请稍后重试')
        else:
            if balance > user.balance:
                raise serializers.ValidationError('提现金额超过本人余额')
        return attrs

    class Meta:
        model = WithDraw
        fields = '__all__'
        read_only_fields = ('id', 'status', 'add_time')


class BankCardListSerializer(serializers.ModelSerializer):
    card_type = serializers.CharField(source='get_card_type_display')
    bank = serializers.CharField(source='get_bank_display')

    class Meta:
        model = BankCard
        fields = ('id', 'card_no', 'card_type', 'is_credit', 'bank', 'add_time')


class BankCardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_phone(self, phone):
        return self.context.get('request').user.mobile

    def validate(self, attrs):
        if attrs.get('card_type', 'DC') == 'DC':
            attrs['is_credit'] = True
            return attrs
        else:
            raise serializers.ValidationError('只能绑定储蓄卡,不能绑定信用卡')

    class Meta:
        model = BankCard
        fields = ('user', 'card_no', 'id_card', 'name', 'card_type', 'bank',
                  'is_credit', 'phone')
