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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rec_dict = serializer.data
        remark = rec_dict.pop('remark')
        company = Company.objects.create(**rec_dict)
        message = '企业认证申请'
        if remark:
            message += '-{}'.format(remark)
        CompanyLog.logging(company=company, user=request.user, message=message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
