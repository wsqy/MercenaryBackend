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

    def validate_card_type(self, card_type):
        if card_type not in settings.BANK_CARD_TYPE:
            return 'unknown'
        return card_type

    def validate_bank(self, bank):
        if bank not in settings.BANK_CARD:
            return 'unknown'
        return bank

    def validate(self, attrs):
        return attrs

    class Meta:
        model = BankCard
        fields = ('user', 'card_no', 'id_card', 'name', 'card_type', 'bank')
