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
    class Meta:
        model = BankCard
        fields = ('card_no', 'card_type', 'is_credit', 'bank', 'add_time')
