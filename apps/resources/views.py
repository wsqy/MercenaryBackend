from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from .models import ResourceMaterial
from .serializers import ResourceMaterialSerializer
from utils.pagination import CommonPagination
from utils.authentication import CommonAuthentication


class ResourceMaterialViewset(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """资源相关接口
    list:
        资源列表
    retrieve:
        资源详情
    """
    queryset = ResourceMaterial.objects.filter(is_active=True)
    pagination_class = CommonPagination
    serializer_class = ResourceMaterialSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('category', )
    authentication_classes = CommonAuthentication()
