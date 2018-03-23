from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin

from .serializers import DeviceRegisterSerializer

User = get_user_model()


class DeviceRegisterViewset(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = DeviceRegisterSerializer
