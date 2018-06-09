import logging
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse

from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin

from .models import PayOrder
from .serializers import PayOrderCreateSerializer
from utils.common import generate_pay_order_id, get_request_ip
from utils.authentication import CommonAuthentication
from utils.pay import alipay, wxpay
from utils.cost import service_cost_calc

logger = logging.getLogger('paycenter.views')


class PayOrderViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin,
                      viewsets.GenericViewSet):
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
        pay_info = ''
        if pay_order_type == 1:
            # 这里是支付押金
            pay_info = '押金支付'
            # 判断当前用户是否为接单者
            if rec_dict['order'].receiver_user.id != rec_dict['user'].id:
                return Response({'user': '当前支付用户不是接单者'},
                                status=status.HTTP_400_BAD_REQUEST)
            # 填充支付订单金额为押金
            rec_dict['pay_cost'] = rec_dict['order'].deposit
            # 订单状态改变
            if rec_dict['order'].status == 12:
                rec_dict['order'].status = 13
                rec_dict['order'].save()
        elif pay_order_type == 3:
            # 这里是支付佣金
            pay_info = '佣金支付'
            # 判断当前用户是否为下单者
            if rec_dict['order'].employer_user.id != rec_dict['user'].id:
                return Response({'user': '当前支付用户不是订单创建者'},
                                status=status.HTTP_400_BAD_REQUEST)
            # 填充支付订单金额为佣金
            rec_dict['pay_cost'] = rec_dict['order'].pay_cost
            # 订单状态改变
            if rec_dict['order'].status == 1:
                rec_dict['order'].status = 2
                rec_dict['order'].save()
        elif pay_order_type == 2:
            # 这里是加赏
            pay_info = '加赏支付'

            # 判断当前用户是否为下单者
            if rec_dict['order'].employer_user.id != rec_dict['user'].id:
                return Response({'user': '当前支付用户不是订单创建者'},
                                status=status.HTTP_400_BAD_REQUEST)
            # 填充支付订单金额为佣金
            rec_dict['pay_cost'] = rec_dict.get('pay_cost', 0) * 100

        # 填充 id
        rec_dict['id'] = generate_pay_order_id(order_type='10')
        # 填充 expire_time
        rec_dict['expire_time'] = timezone.now() + timezone.timedelta(seconds=settings.ALIPAT_EXPIRE_TIME)

        rec_dict['status'] = 2

        self.perform_create(serializer)
        return self.generate_payorder(request, pay_info, rec_dict)

    def generate_payorder(self, request, pay_desc, rec_dict):
        """
        生成支付订单信息
        :param rec_dict:
        :return:
        """
        # 生成支付信息
        if rec_dict['pay_method'] == 1:
            pay_info = alipay.app_pay(
                subject='{}-{}'.format(pay_desc, rec_dict['order'].description),
                out_trade_no=rec_dict['id'],
                total_amount=rec_dict['pay_cost'] / 100,
            )
        elif rec_dict['pay_method'] == 2:
            pay_info = wxpay.app_pay(
                body='{}-{}'.format(pay_desc, rec_dict['order'].description),
                out_trade_no=rec_dict['id'],
                total_fee=rec_dict['pay_cost'],
                spbill_create_ip=get_request_ip(request),
                trade_type='APP'
            )
        response_dict = {
            'pay_info': pay_info
        }

        return Response(response_dict, status=status.HTTP_201_CREATED)


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
        logger.debug('支付宝回调参数{}'.format(request.POST))
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop('sign', None)

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

        existed_pay_orders = PayOrder.objects.filter(id=pay_order_id, status=2)
        for existed_pay_order in existed_pay_orders:
            # 金额不符合 跳过
            if existed_pay_order.pay_cost != pay_total_amount:
                continue

            if existed_pay_order.order_type == 3:
                # 如果是佣金支付成功则设置订单状态为 待接单
                existed_pay_order.order.status = 11
                existed_pay_order.order.save()
            elif existed_pay_order.order_type == 1:
                # 如果是押金支付则设置订单状态为 进行中
                existed_pay_order.order.status = 20
                existed_pay_order.order.save()
            elif existed_pay_order.order_type == 2:
                # 加赏
                # 接单前 有抽成
                logger.debug('原先支付金额-{};原先商金-{}'.format(existed_pay_order.order.pay_cost, existed_pay_order.order.reward))
                if existed_pay_order.order.status == 11:
                    existed_pay_order.order.pay_cost += pay_total_amount
                    existed_pay_order.order.reward += (pay_total_amount - service_cost_calc.calc(pay_total_amount))
                    logger.debug('最新支付金额-{};最新商金-{}'.format(existed_pay_order.order.pay_cost, existed_pay_order.order.reward))
                    existed_pay_order.order.save()
                # 接单后加赏 等同于打赏 不需要抽成
                else:
                    existed_pay_order.order.pay_cost += pay_total_amount
                    existed_pay_order.order.reward += pay_total_amount
                    existed_pay_order.order.save()

            existed_pay_order.status = 3
            existed_pay_order.pay_time = timezone.now()
            existed_pay_order.save()

        return HttpResponse('success')
