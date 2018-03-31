import json
import string
import random

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from rest_framework import viewsets
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from utils.dayu import DaYuSMS
from .serializers import DeviceRegisterSerializer, SmsSerializer, UserRegSerializer
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
    发送短信验证
    """
    serializer_class = SmsSerializer

    def generate_code(self, CODE_LENGTH=4):
        """
        生成四位数字的验证码
        :return:
        random.sample 从指定的序列中，随机的截取指定长度的片断
        """
        return ''.join(random.sample(string.digits, CODE_LENGTH))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        type = serializer.validated_data['type']
        code = self.generate_code()

        dayun_sms = DaYuSMS(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)
        sms_params = {
            'code': code,
            'time': settings.REGEISTER_SMS_EXPIRE_TIME_DEFAULT
        }
        sms_ststus = dayun_sms.send_sms(phone_numbers=mobile, template_code='SMS_76310006', template_param=json.dumps(sms_params))

        try:
            sms_ststus_dict = json.loads(bytes.decode(sms_ststus))
            sms_code = sms_ststus_dict.get('Code', None)
            assert sms_code is not None
            sms_status_msg = DaYuSMS.DaYuSMS_STATUS.get(sms_code, 'UNKNOWN_ERROR')
            if sms_code == 'OK':
                expire_time = timezone.now() + timezone.timedelta(seconds=settings.VERIFY_CODE_EXPIRE_TIME)
                VerifyCode.objects.create(code=code, mobile=mobile, type=type, expire_time=expire_time)
                return Response({'msg': sms_status_msg}, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg': sms_status_msg}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'msg': '短信服务异常, 请稍后重试'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewset(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserRegSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        payload = jwt_payload_handler(user)
        re_dict = serializer.data
        re_dict['token'] = jwt_encode_handler(payload)

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
