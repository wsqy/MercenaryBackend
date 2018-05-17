from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
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

    def validate(self, attrs):
        _type = attrs.get('type')
        _mobile = attrs.get('mobile')
        user_count = User.objects.filter(username=_mobile)
        # 注册 要求 手机号不存在
        if _type == settings.REGISTER_CODE_TYPE:
            if user_count:
                raise serializers.ValidationError('该手机号已注册')
        # 重置密码 要求 手机号已存在
        elif _type == settings.FORGET_PASSWD_CODE_TYPE:
            if not user_count:
                raise serializers.ValidationError('该手机号未在平台注册')
        return attrs

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
        user.set_password(validated_data['password'])
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

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        attrs['nickname'] = '用户{}'.format(attrs['username'][-4:])
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'code', 'mobile', 'password', 'nickname')


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'nickname', 'gender',
                  'portrait', 'first_name', 'date_joined', 'last_login')


class UserOrderListSerializer(serializers.ModelSerializer):
    """
    订单列表用户序列化类
    """
    class Meta:
        model = User
        fields = ('nickname', 'portrait',)


class UserOrderDetailSerializer(serializers.ModelSerializer):
    """
    订单详情用户序列化类
    """
    class Meta:
        model = User
        fields = ('id', 'mobile', 'nickname', 'gender', 'portrait',)


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    用户信息修改序列化类
    """
    class Meta:
        model = User
        fields = ('nickname', 'gender', 'portrait',)


class UserPortraitSerializer(serializers.Serializer):
    """
    异步头像上传
    """
    portrait = serializers.ImageField(max_length=79, allow_empty_file=False, required=False)


class PasswordResetSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, min_length=11, label='手机号',
                                   help_text='注册手机号',
                                   error_messages={
                                       'blank': '请输入注册手机号',
                                       'required': '请输入注册手机号',
                                       'max_length': '手机号格式错误',
                                       'min_length': '手机号格式错误'
                                   })
    password_new = serializers.CharField(style={'input_type': 'password'},
                                         help_text='新密码', label='新密码',
                                         min_length=6,
                                         error_messages={
                                             'blank': '请输入新密码',
                                             'required': '请输入新密码',
                                             'min_length': '密码至少6位'
                                         })
    code = serializers.CharField(label='验证码', help_text='验证码',
                                 max_length=4, min_length=4,
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误'
                                 })

    def validate_mobile(self, mobile):
        users = User.objects.filter(username=mobile)
        if not users.count():
            raise serializers.ValidationError('用户名不存在')
        return mobile

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['mobile'],
                                                   type=settings.FORGET_PASSWD_CODE_TYPE,
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
        return code


class PasswordModifySerializer(serializers.Serializer):
    password_old = serializers.CharField(style={'input_type': 'password'},
                                         help_text='密码', label='密码',
                                         error_messages={
                                             'blank': '请输入原始密码',
                                             'required': '请输入原始密码',
                                         })
    password_new = serializers.CharField(style={'input_type': 'password'},
                                         help_text='新密码', label='新密码',
                                         min_length=6,
                                         error_messages={
                                             'blank': '请输入新密码',
                                             'required': '请输入新密码',
                                             'min_length': '密码至少6位'
                                         })

    def validate(self, attrs):
        if attrs.get('password_old') == attrs.get('password_new'):
            raise serializers.ValidationError('两次密码不能一致')
        return attrs
