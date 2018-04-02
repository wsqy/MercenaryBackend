from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from .models import DeviceInfo, VerifyCode
from utils.aliyun_oss import Oss

User = get_user_model()


class DeviceRegisterSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = DeviceInfo
        fields = ('deviceid', 'model', 'device_ver', 'channel_code')


class SmsSerializer(serializers.ModelSerializer):
    def validate_type(self, _type):
        if _type not in settings.CODE_TYPE:
            raise serializers.ValidationError('验证码类型错误')
        return _type

    class Meta:
        model = VerifyCode
        fields = ('type', 'mobile')


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4,
                                 label='验证码',help_text='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误'
                                 })
    username = serializers.CharField(label='用户名', help_text='用户名', required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已经存在')])

    password = serializers.CharField(style={'input_type': 'password'}, help_text='密码',
                                     label='密码', write_only=True)

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username'],
                                                   type=settings.REGISTER_CODE_TYPE,
                                                   expire_time__gte=timezone.now())
        if verify_records:
            last_record = verify_records[0]
            if last_record.code != code:
                if last_record.try_time <= 1:
                    last_record.try_time = 0
                    last_record.save()
                    raise serializers.ValidationError('验证码错误, 请重新获取')
                else:
                    last_record.try_time -= 1
                    last_record.save()
                    raise serializers.ValidationError('验证码错误, 还剩{}次重试机会'.format(last_record.try_time))
        else:
            raise serializers.ValidationError('请先获取验证码')

    def validate(self, params):
        params['mobile'] = params['username']
        params['nickname'] = '用户{}'.format(params['username'][-4:])
        del params['code']
        return params

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password', 'nickname')


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'email', 'nickname', 'gender', 'portrait', 'mobile')


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    用户信息修改序列化类
    """
    portrait = serializers.ImageField(max_length=79, allow_empty_file=True)

    def validate_portrait(self, portrait):
        oss = Oss()
        oss.user_upload_portrait(portrait.file, portrait._name)

    class Meta:
        model = User
        fields = ('nickname', 'gender', 'portrait')
