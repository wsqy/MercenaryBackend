from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Company, CompanyLog, PartTimeOrder, PartTimeOrderCard
from .serializers import (
    CompanyInfoSerializer, CompanyListSerializer, CompanyCreateSerializer,
    PartTimeOrderInfoSerializer, PartTimeOrderListSerializer, PartTimeOrderCreateSerializer,
    PartTimeOrderCardSerializer
)
from .filters import PartTimeOrderFilter

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
        elif self.action == 'application':
            return CompanyInfoSerializer
        elif self.action == 'create':
            return CompanyCreateSerializer
        return CompanyInfoSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            queryset = queryset.filter(status=30)
        return queryset

    def get_object(self):
        if self.action == 'retrieve':
            return super(CompanyViewset, self).get_object()
        elif self.action == 'application':
            return  Company.objects.filter(user=self.request.user).first()

    @action(methods=['get'], detail=False)
    def application(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PartTimeOrderViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    """兼职招募令相关接口
    list:
        招募令列表
    retrieve:
        招募令详情
    create:
        新建招募令
    update:
        修改招募令信息
    """
    queryset = PartTimeOrder.objects.all()
    pagination_class = CommonPagination
    authentication_classes = CommonAuthentication()

    filter_backends = (DjangoFilterBackend,)
    filter_class = PartTimeOrderFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return PartTimeOrderListSerializer
        elif self.action == 'create':
            return PartTimeOrderCreateSerializer
        return PartTimeOrderInfoSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset


class PartTimeOrderCardViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    """兼职招募令卡片相关接口
    list:
        卡片列表
    retrieve:
        卡片详情
    create:
        新建卡片
    update:
        修改卡片信息
    """
    queryset = PartTimeOrderCard.objects.all()
    pagination_class = CommonPagination
    # authentication_classes = CommonAuthentication()
    def get_serializer_class(self):
        return PartTimeOrderCardSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset
