from rest_framework import serializers

from .models import SubCategory, OrderInfo, OrdersImage
from users.serializers import UserOrderListSerializer, UserOrderDetailSerializer
from area.serializers import SchoolSerializer


class SubCategorySerializer(serializers.ModelSerializer):
    classification = serializers.CharField(source='get_classification_display')

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'template', 'classification')


class OrdersImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersImage
        fields = ('image', )


class OrderInfoSerializer(serializers.ModelSerializer):
    # category = SubCategorySerializer()
    category = serializers.CharField(source='get_category_display')
    status_name = serializers.CharField(source='get_status_display')
    employer_user = UserOrderDetailSerializer()
    receiver_user = UserOrderDetailSerializer()
    school = SchoolSerializer()
    reward = serializers.SerializerMethodField()
    is_employer_user = serializers.SerializerMethodField()
    is_receiver_user = serializers.SerializerMethodField()
    images = OrdersImageSerializer(many=True)

    def get_is_employer_user(self, obj):
        return self.context.get('request').user == obj.employer_user

    def get_is_receiver_user(self, obj):
        return self.context.get('request').user == obj.receiver_user

    def get_reward(self, obj):
        if self.context.get('request').user == obj.employer_user:
            return obj.pay_cost
        else:
            return obj.reward

    class Meta:
        model = OrderInfo
        exclude = ('pay_cost', )


class OrderInfoCreateSerializer(serializers.ModelSerializer):
    employer_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    images = OrdersImageSerializer(many=True)

    class Meta:
        model = OrderInfo
        read_only_fields = ('id', 'status', 'create_time', 'reward',)
        exclude = ('complete_time', 'employer_complete_time', 'receiver_confirm_time',
                   'receiver_complete_time', 'receiver_user')


class OrderInfoListSerializer(serializers.ModelSerializer):
    employer_user = UserOrderListSerializer()
    # category = SubCategorySerializer()
    category = serializers.CharField(source='get_category_display')
    status_name = serializers.CharField(source='get_status_display')
    reward = serializers.SerializerMethodField()

    def get_reward(self, obj):
        if self.context.get('request').user == obj.employer_user:
            return obj.pay_cost
        else:
            return obj.reward

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderInfoReceiptSerializer(serializers.ModelSerializer):
    reward = serializers.SerializerMethodField()

    def get_reward(self, obj):
        if self.context.get('request').user == obj.employer_user:
            return obj.pay_cost
        else:
            return obj.reward

    class Meta:
        model = OrderInfo
        fields = ('id', 'status', 'deposit', 'reward', 'pay_cost')
        read_only_fields = ('status', 'deposit', 'reward', 'pay_cost')
