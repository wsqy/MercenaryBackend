from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from .models import Company
from .serializers import CompanyInfoSerializer, CompanyListSerializer
from utils.pagination import CommonPagination
from utils.authentication import CommonAuthentication


class CompanyViewset(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """公司相关接口
    list:
        公司列表
    retrieve:
        公司详情
    """
    queryset = Company.objects.all()
    pagination_class = CommonPagination
    authentication_classes = CommonAuthentication()

    def get_serializer_class(self):
        if self.action == 'list':
            return CompanyListSerializer
        elif self.action == 'retrieve':
            return CompanyInfoSerializer
        return CompanyListSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            queryset = queryset.filter(status=30)
        return queryset
