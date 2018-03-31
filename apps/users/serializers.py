from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import DeviceInfo, VerifyCode

User = get_user_model()


class DeviceRegisterSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = DeviceInfo
        fields = ('deviceid', 'model', 'device_ver', 'channel_code')


class SmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyCode
        fields = ('type', 'mobile')


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误'
                                 },
                                 help_text='验证码')
    username = serializers.CharField(label='用户名', help_text='用户名', required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已经存在')])

    password = serializers.CharField(style={'input_type': 'password'}, help_text='密码', label='密码', write_only=True)

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username'],
                                                   type='SMS_76310006', expire_time__gte=timezone.now())
        if verify_records:
            last_record = verify_records[0]
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, params):
        params['mobile'] = params['username']
        del params['code']
        return params

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password')
