from rest_framework import serializers

from .models import SubCategory, OrderInfo


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'template')


class OrderInfoCreateSerializer(serializers.ModelSerializer):
    employer_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = OrderInfo
        read_only_fields = ('id', 'status', 'create_time', 'reward',)
        exclude = ('complete_time', 'employer_complete_time', 'receiver_confirm_time',
                   'receiver_complete_time', 'receiver_user')


class OrderInfoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderInfoReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ('id', 'status', 'deposit', 'reward', 'pay_cost')
        read_only_fields = ('status', 'deposit', 'reward', 'pay_cost')
