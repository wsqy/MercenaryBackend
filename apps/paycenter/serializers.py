from rest_framework import serializers

from .models import PayOrder, PartTimePayOrder


class PayOrderCreateSerializer(serializers.ModelSerializer):
    # todo order不合法的提示语

    pay_cost = serializers.IntegerField(default=1, label='支付金额(分)',
                                        help_text='支付金额(分)',)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = PayOrder
        read_only_fields = ('id', 'status', 'create_time', 'expire_time',)
        exclude = ('pay_time',)


class PayReturnSerializer(serializers.Serializer):
    pass



class PartTimePayOrderCreateSerializer(serializers.ModelSerializer):
    pay_cost = serializers.IntegerField(default=0, label='支付金额(分)',
                                        help_text='支付金额(分)',)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = PartTimePayOrder
        read_only_fields = ('id', 'status', 'create_time', 'expire_time', 'pay_time', 'pay_cost', 'order_type')
        fields = '__all__'
