from rest_framework import serializers

from .models import SubCategory, OrderInfo
from users.serializers import UserDetailSerializer
from area.serializers import DistrictInfoSerializer


class SubCategorySerializer(serializers.ModelSerializer):
    classification = serializers.CharField(source='get_classification_display')

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'template', 'classification')


class OrderInfoSerializer(serializers.ModelSerializer):
    category = SubCategorySerializer()
    status_name = serializers.CharField(source='get_status_display')
    employer_user = UserDetailSerializer()
    receiver_user = UserDetailSerializer()
    from_addr_district = DistrictInfoSerializer()
    to_addr_district = DistrictInfoSerializer()
    create_district = DistrictInfoSerializer()

    class Meta:
        model = OrderInfo
        fields = '__all__'


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
    category = SubCategorySerializer()
    status_name = serializers.CharField(source='get_status_display')

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderInfoReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ('id', 'status', 'deposit', 'reward', 'pay_cost')
        read_only_fields = ('status', 'deposit', 'reward', 'pay_cost')
