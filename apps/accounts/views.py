from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin

from .models import BalanceDetail, BankCard
from users.models import ProfileExtendInfo
from .serializers import BalanceSerializer, BalanceListSerializer, BankCardListSerializer

from utils.pagination import CommonPagination
from utils.authentication import CommonAuthentication


class BalanceViewset(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = BalanceDetail.objects.all()
    authentication_classes = CommonAuthentication()
    pagination_class = CommonPagination

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BalanceSerializer
        elif self.action == 'list':
            return BalanceListSerializer

    def get_object(self):
        return ProfileExtendInfo.objects.get(user=self.request.user)

    def get_queryset(self):
        if self.action == 'list':
            queryset = self.queryset.filter(user=self.request.user)

        return queryset


class BankCardViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin,
                      viewsets.GenericViewSet):
    """银行卡相关接口
    list:
        订单发现页列表
    create:
        下单
    retrieve:
    """
    queryset = BankCard.objects.all()
    authentication_classes = CommonAuthentication()
    pagination_class = CommonPagination

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return BalanceSerializer
        elif self.action == 'list':
            return BankCardListSerializer
        elif self.action == 'retrieve':
            return BalanceListSerializer

    def get_queryset(self):
        if self.action == 'list':
            queryset = self.queryset.filter(user=self.request.user, is_activate=True)
        return queryset
