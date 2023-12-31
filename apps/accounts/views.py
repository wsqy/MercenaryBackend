import logging
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
)
from rest_framework.response import Response

from .models import BalanceDetail, BankCard, WithDraw
from users.models import ProfileExtendInfo
from .serializers import (
    BalanceSerializer, BalanceListSerializer, WithDrawCreateSerializer,
    BankCardListSerializer, BankCardCreateSerializer, WithDrawListSerializer
)

from utils.pagination import CommonPagination
from utils.authentication import CommonAuthentication
from utils.bank_card import realname_authentication


logger = logging.getLogger('accounts')

class BalanceViewset(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """余额相关相关接口
    list:
        余额变动接口
    retrieve:
        余额查询
    """
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
        return BalanceSerializer

    def get_object(self):
        return ProfileExtendInfo.objects.get(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            queryset = queryset.filter(user=self.request.user)

        return queryset


class BankCardViewset(ListModelMixin, CreateModelMixin, DestroyModelMixin,
                      viewsets.GenericViewSet):
    """银行卡相关接口
    list:
        银行卡列表
    create:
        绑定银行卡
    destroy:
        解除银行卡的绑定
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
        serializer.is_valid(raise_exception=True)
        rec_dict = serializer.validated_data
        filter_res = BankCard.objects.filter(card_no=rec_dict.get('card_no', ''))
        if filter_res.count() != 0:
            for filter_one in filter_res:
                if filter_one.name != rec_dict.get('name'):
                    return Response({'msg': '验证失败,姓名填写错误'}, status=status.HTTP_403_FORBIDDEN)
                if filter_one.user != rec_dict.get('user'):
                    return Response({'msg': '验证失败, 该银行已被绑定, 如有疑问, 请联系客服处理'}, status=status.HTTP_403_FORBIDDEN)
                if filter_one.id_card != rec_dict.get('id_card'):
                    return Response({'msg': '验证失败, 身份证填写错误'}, status=status.HTTP_403_FORBIDDEN)
                filter_one.is_activate = True
                filter_one.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        auth_res = realname_authentication(
            acct_pan=rec_dict.get('card_no'),
            acct_name=rec_dict.get('name'),
            cert_id=rec_dict.get('id_card'),
            phone_num=self.request.user.mobile,
        )

        if auth_res.get('resp', {}).get('code') == 0:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            logger.error('绑定银行卡失败,错误信息:{}'.format(auth_res))
            return Response({'msg': '验证失败,请检查填写是否正确'}, status=status.HTTP_403_FORBIDDEN)


class WithDrawViewset(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    """提现相关接口
    list:
        提现记录
    create:
        提现申请
    """
    queryset = WithDraw.objects.all()
    authentication_classes = CommonAuthentication()
    pagination_class = CommonPagination

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return WithDrawCreateSerializer
        elif self.action == 'list':
            return WithDrawListSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'list':
            queryset = queryset.filter(user=self.request.user)

        return queryset
