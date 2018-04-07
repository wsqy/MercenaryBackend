import json
import string
import random

from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.backends import ModelBackend

from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler


from utils.dayu import DaYuSMS
from .serializers import DeviceRegisterSerializer, SmsSerializer
from .serializers import UserRegSerializer, UserDetailSerializer, UserUpdateSerializer
from .serializers import PasswordResetSerializer, PasswordModifySerializer
from .models import VerifyCode, DeviceInfo

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class DeviceRegisterViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        设备注册
    """
    serializer_class = DeviceRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        deviceid = serializer.validated_data['deviceid']
        try:
            DeviceInfo.objects.get(deviceid=deviceid)
            return Response({'deviceid': deviceid}, status=status.HTTP_202_ACCEPTED)
        except DeviceInfo.DoesNotExist:
            self.perform_create(serializer)
            return Response({'deviceid': deviceid}, status=status.HTTP_201_CREATED)


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        发送短信验证
    """
    serializer_class = SmsSerializer

    @staticmethod
    def generate_code(code_len=4):
        """
        生成四位数字的验证码
        :return:
        random.sample 从指定的序列中，随机的截取指定长度的片断
        """
        return ''.join(random.sample(string.digits, code_len))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sms_mobile = serializer.validated_data['mobile']
        sms_type = serializer.validated_data['type']
        sms_code = self.generate_code()

        dayun_sms = DaYuSMS()
        sms_params = {
            'code': sms_code,
            'time': settings.REGEISTER_SMS_EXPIRE_TIME_DEFAULT
        }

        sms_status = dayun_sms.send_sms(phone_numbers=sms_mobile,
                                        template_code=sms_type,
                                        template_param=json.dumps(sms_params))

        try:
            sms_status_dict = json.loads(bytes.decode(sms_status))
            sms_status_code = sms_status_dict.get('Code', None)
            assert sms_status_code is not None
            sms_status_msg = DaYuSMS.DaYuSMS_STATUS.get(sms_status_code, 'UNKNOWN_ERROR')
            if sms_status_code == 'OK':
                sms_expire_time = timezone.now() + timezone.timedelta(seconds=settings.VERIFY_CODE_EXPIRE_TIME)
                VerifyCode.objects.create(code=sms_code, mobile=sms_mobile,
                                          type=sms_type, expire_time=sms_expire_time)
                return Response({'msg': sms_status_msg}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': sms_status_msg}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg': '短信服务异常, 请稍后重试'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewset(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    """用户相关接口
    create:
        用户注册
    retrieve:
        获取用户信息
    Update:
        用户信息修改,忘记密码，修改密码
    """
    serializer_class = UserRegSerializer
    # authentication_classes = (JSONWebTokenAuthentication,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        elif self.action == 'update':
            return UserUpdateSerializer
        elif self.action == 'reset_password':
            return PasswordResetSerializer
        elif self.action == 'modify_password':
            return PasswordModifySerializer
        elif self.action == 'login':
            return JSONWebTokenSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'reset_password', 'login']:
            return []
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        return serializer.save()

    def get_object(self):
        return self.request.user

    def get_user_info(self, instance):
        instance.last_login = timezone.now()
        instance.save()
        serializer = UserDetailSerializer(instance)
        re_dict = serializer.data
        if re_dict.get('portrait'):
            re_dict['portrait'] = 'https://{}.{}/{}'.format(settings.BUCKET_NAME,
                                                            settings.END_POINT,
                                                            re_dict['portrait'])
        return re_dict

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        payload = jwt_payload_handler(user)
        re_dict = self.get_user_info(user)
        re_dict['token'] = jwt_encode_handler(payload)

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(self.get_user_info(instance))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(self.get_user_info(instance))

    @action(methods=['patch'], detail=True)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(username=serializer.validated_data.get('mobile'))[0]
        user.set_password(serializer.validated_data.get('password_new'))
        user.save()
        re_dict = {'msg': '密码重置成功'}
        return Response(re_dict)

    @action(methods=['patch'], detail=True)
    def modify_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        _password_new = serializer.validated_data.get('password_new')
        _password_old = serializer.validated_data.get('password_old')
        check_user = authenticate(username=instance.username, password=_password_old)
        if check_user is None:
            return Response({'msg': '原密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            instance.set_password(_password_new)
            instance.save()
        return Response(self.get_user_info(instance))

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')
        response_data = self.get_user_info(user)
        response_data['token'] = serializer.object.get('token')
        response = Response(response_data)

        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() +
                          api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                token,
                                expires=expiration,
                                httponly=True)
        return response
