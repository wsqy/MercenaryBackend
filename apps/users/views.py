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

from .serializers import DeviceRegisterSerializer, SmsSerializer
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
        deviceid = serializer.validated_data["deviceid"]
        try:
            DeviceInfo.objects.get(deviceid=deviceid)
            return Response({"deviceid": deviceid}, status=status.HTTP_202_ACCEPTED)
        except DeviceInfo.DoesNotExist:
            self.perform_create(serializer)
            return Response({"deviceid": deviceid}, status=status.HTTP_201_CREATED)


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self, CODE_LENGTH=None):
        """
        生成四位数字的验证码
        :return:
        random.sample 从指定的序列中，随机的截取指定长度的片断
        """
        if CODE_LENGTH is None:
            CODE_LENGTH = 4
        return "".join(random.sample(string.digits, CODE_LENGTH))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]
        type = serializer.validated_data["type"]

        code = self.generate_code()
        expire_time = timezone.now() + timezone.timedelta(
                       seconds=settings.VERIFY_CODE_EXPIRE_TIME)
        code_record = VerifyCode(code=code, mobile=mobile, type=type,
                                 expire_time=expire_time)
        code_record.save()
        return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)
