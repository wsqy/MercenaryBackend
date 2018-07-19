from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response

from .models import Company, CompanyLog
from .serializers import CompanyInfoSerializer, CompanyListSerializer, CompanyCreateSerializer
from utils.pagination import CommonPagination
from utils.authentication import CommonAuthentication


class CompanyViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    """公司相关接口
    list:
        公司列表
    retrieve:
        公司详情
    create:
        公司认证
    """
    queryset = Company.objects.all()
    pagination_class = CommonPagination
    authentication_classes = CommonAuthentication()

    def get_serializer_class(self):
        if self.action == 'list':
            return CompanyListSerializer
        elif self.action == 'retrieve':
            return CompanyInfoSerializer
        elif self.action == 'create':
            return CompanyCreateSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            queryset = queryset.filter(status=30)
        return queryset
