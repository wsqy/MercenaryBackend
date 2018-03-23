from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import DeviceInfo

User = get_user_model()


class DeviceRegisterSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = DeviceInfo
        fields = ("deviceid", "model", "device_ver", "channel_code")
