from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
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
            # 这里是支付押金

            # 判断当前用户是否为接单者
            if rec_dict['order'].receiver_user.id != rec_dict['user'].id:
                return Response({'user': '当前支付用户不是接单者'}, status=status.HTTP_400_BAD_REQUEST)
            # 填充支付订单金额为押金
            rec_dict['pay_cost'] = rec_dict['order'].deposit
            # 订单状态改变
            if rec_dict['order'].status == 12:
                rec_dict['order'].status = 13
                rec_dict['order'].save()
        elif pay_order_type == 3:
            # 这里是支付佣金

            # 判断当前用户是否为下单者
            if rec_dict['order'].employer_user.id != rec_dict['user'].id:
                return Response({'user': '当前支付用户不是订单创建者'}, status=status.HTTP_400_BAD_REQUEST)
            # 填充支付订单金额为佣金
            rec_dict['pay_cost'] = rec_dict['order'].pay_cost
            # 订单状态改变
            if rec_dict['order'].status == 1:
                rec_dict['order'].status = 2
                rec_dict['order'].save()
        elif pay_order_type == 2:
            # 这里是加赏
            pass

        # 填充 id
        rec_dict['id'] = generate_pay_order_id(order_type='10')
        # 填充 expire_time
        rec_dict['expire_time'] = timezone.now() + timezone.timedelta(seconds=settings.ALIPAT_EXPIRE_TIME)

        rec_dict['status'] = 2

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


class AlipayView(APIView):
    """
    支付宝支付相关处理
    """
    def post(self, request):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        verify_re = alipay.verify(processed_dict, sign)

        # 验签不过的消息不管
        if verify_re is False:
            return Response({'msg': 'verify error'}, status.HTTP_401_UNAUTHORIZED)

        pay_order_id = processed_dict.get('out_trade_no', None)
        trade_status = processed_dict.get('trade_status', None)
        pay_total_amount = float(processed_dict.get('total_amount', 0)) * 100
        # 只接受 交易成功的消息
        if trade_status != 'TRADE_SUCCESS':
            return Response({'msg': 'status unsuccess'}, status.HTTP_100_CONTINUE)

        existed_pay_orders = PayOrder.objects.filter(id=pay_order_id)
        for existed_pay_order in existed_pay_orders:
            # 金额不符合 跳过
            if existed_pay_order.pay_cost != pay_total_amount:
                continue
            existed_pay_order.status = 3
            existed_pay_order.pay_time = timezone.now()
            existed_pay_order.save()
            if existed_pay_order.order_type == 3:
                # 如果是佣金支付成功则设置订单状态为 待接单
                existed_pay_order.order.status = 11
                existed_pay_order.order.save()
            elif existed_pay_order.order_type == 1:
                # 如果是押金支付则设置订单状态为 进行中
                existed_pay_order.order.status = 20
                existed_pay_order.order.save()
        return Response("success")
