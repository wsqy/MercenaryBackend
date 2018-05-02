from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from .models import PayOrder
from .serializers import PayOrderCreateSerializer
from utils.common import generate_pay_order_id
from utils.authentication import CommonAuthentication
from utils.pay import alipay


class PayOrderViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = PayOrder.objects.all()
    authentication_classes = CommonAuthentication()

    def get_permissions(self):
        if self.action in ['create', ]:
            return [permissions.IsAuthenticated()]
        return []

    def get_serializer_class(self):
        if self.action == 'create':
            return PayOrderCreateSerializer
        return PayOrderCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rec_dict = serializer.validated_data

        pay_order_type = rec_dict['order_type']

        # 根据 订单号和order_type 判断user信息是否合法
        # 填充 pay_cost
        if pay_order_type == 1:
            rec_dict['pay_cost'] = rec_dict['order'].deposit
            if rec_dict['order'].receiver_user is not rec_dict['user']:
                return Response({'user': '当前支付用户不是接单者'}, status=status.HTTP_400_BAD_REQUEST)
        elif pay_order_type == 3:
            rec_dict['pay_cost'] = rec_dict['order'].pay_cost
            if rec_dict['order'].employer_user.id is not rec_dict['user'].id:
                return Response({'user': '当前支付用户不是订单创建者'}, status=status.HTTP_400_BAD_REQUEST)

        # 填充 id
        rec_dict['id'] = generate_pay_order_id(order_type='10')
        # 填充 expire_time
        rec_dict['expire_time'] = timezone.now() + timezone.timedelta(seconds=settings.ALIPAT_EXPIRE_TIME)

        self.perform_create(serializer)
        # 生成支付信息
        pay_info = alipay.app_pay(
            subject='雇佣兵-佣金支付',
            out_trade_no=rec_dict['id'],
            total_amount=rec_dict['pay_cost'] / 100,
        )

        headers = self.get_success_headers({'pay_info': pay_info})
        # rec_dict['pay_info'] = pay_info
        return Response({'pay_info': pay_info}, status=status.HTTP_201_CREATED, headers=headers)
