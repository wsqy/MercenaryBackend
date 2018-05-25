from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
)

from .models import BalanceDetail, BankCard
from users.models import ProfileExtendInfo
from .serializers import (
    BalanceSerializer, BalanceListSerializer,
    BankCardListSerializer, BankCardCreateSerializer
)

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


class BankCardViewset(ListModelMixin, CreateModelMixin, DestroyModelMixin,
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
            return BankCardCreateSerializer
        elif self.action == 'list':
            return BankCardListSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            queryset = queryset.filter(user=self.request.user, is_activate=True)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == self.request.user:
            instance.is_activate = False
            instance.save()
            return Response({'msg': '删除成功'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': '只能删除本人账号下的银行卡'},
                            status=status.HTTP_403_FORBIDDEN)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)