from django.conf import settings
from rest_framework import serializers

from .models import BalanceDetail, BankCard
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


class BankCardListSerializer(serializers.ModelSerializer):
    card_type = serializers.CharField(source='get_card_type_display')
    bank = serializers.CharField(source='get_bank_display')
    
    class Meta:
        model = BankCard
        fields = ('id', 'card_no', 'card_type', 'is_credit', 'bank', 'add_time')


class BankCardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        if attrs.get('card_type', 'DC') == 'DC':
            attrs['is_credit'] = True
            return attrs
        else:
            raise serializers.ValidationError('只能绑定储蓄卡,不能绑定信用卡')

    class Meta:
        model = BankCard
        fields = ('user', 'card_no', 'id_card', 'name', 'card_type', 'bank', 'is_credit')
