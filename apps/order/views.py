from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import SubCategory, OrderInfo
from .serializers import SubCategorySerializer, OrderInfoSerializer, OrderInfoCreateSerializer, OrderInfoListSerializer, OrderInfoReceiptSerializer
from utils.common import generate_order_id
from utils.authentication import CommonAuthentication
from utils.cost import service_cost_calc
from .tasks import order_deposit_pay_timeout_monitor, order_reward_pay_timeout_monitor, order_reward_pay_refund_monitor
from .filters import OrderFilter


class SubCategoryViewset(ListModelMixin, viewsets.GenericViewSet):
    queryset = SubCategory.objects.filter(is_active=True)
    serializer_class = SubCategorySerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('classification', )


class GoodsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 10


class OrderViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """订单相关接口
    list:
        订单发现页列表
    create:
        下单
    retrieve:
        获取订单信息
    release:
        我发布订单列表
    service:
        我服务订单列表
    receipt:
        接单
    find:
        发现页列表
    cancel:
        取消订单
    complete:
        订单确认完成
    """
    authentication_classes = CommonAuthentication()
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = OrderFilter
    # filter_fields = ('status', 'deposit')
    ordering_fields = ('reward', )

    def get_permissions(self):
        if self.action in ['find', ]:
            return []
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderInfoCreateSerializer
        elif self.action == 'receipt':
            return OrderInfoReceiptSerializer
        elif self.action in ['find', 'release', 'service']:
            return OrderInfoListSerializer
        elif self.action in ['retrieve']:
            return OrderInfoSerializer
        return OrderInfoSerializer

    @staticmethod
    def get_order_info(instance):
        serializer = OrderInfoSerializer(instance)
        return serializer.data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rec_dict = serializer.validated_data

        rec_dict['id'] = generate_order_id(order_type='10')
        if not rec_dict.get('employer_receive_name'):
            rec_dict['employer_receive_name'] = rec_dict['employer_user'].nickname
        if not rec_dict.get('employer_receive_mobile'):
            rec_dict['employer_receive_mobile'] = rec_dict['employer_user'].mobile
        rec_dict['reward'] = rec_dict['pay_cost'] - service_cost_calc.calc(rec_dict['pay_cost'])

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 下单30分钟后查看订单佣金支付状态
        order_reward_pay_timeout_monitor.apply_async(args=(rec_dict['id'],),
                                                     eta=datetime.utcnow() +
                                                     timedelta(seconds=settings.PAY_DEFAULT_EXPIRE_TIME))
        # 订单 to_time 到期 查询 订单是否未接,进行是否退押金步骤
        order_reward_pay_refund_monitor.apply_async(args=(rec_dict['id'], -23), eta=rec_dict['to_time'])
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        if self.action == 'release':
            queryset = OrderInfo.objects.filter(employer_user=self.request.user.id)
        elif self.action == 'service':
            queryset = OrderInfo.objects.filter(receiver_user=self.request.user.id)
        elif self.action == 'find':
            queryset = OrderInfo.objects.filter(status=11, to_time__gt=timezone.now())
        else:
            queryset = OrderInfo.objects.all()
        return queryset

    @action(methods=['get'], detail=False)
    def release(self, request, *args, **kwargs):
        # 我发布的订单
        return self.list(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def service(self, request, *args, **kwargs):
        # 我服务的订单
        return self.list(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def find(self, request, *args, **kwargs):
        # 发现页订单列表
        return self.list(request, *args, **kwargs)

    @action(methods=['patch'], detail=True)
    def receipt(self, request, *args, **kwargs):
        # 接单
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({'msg': '订单不存在'}, status=status.HTTP_400_BAD_REQUEST)
        # 判断接单者是否是订单创建者
        if request.user is instance.employer_user:
            return Response({'msg': '不能接自己的订单'}, status=status.HTTP_400_BAD_REQUEST)

        # 订单状态判断
        if instance.status < 0:
            return Response({'msg': '订单已被取消,换个订单看下吧'}, status=status.HTTP_400_BAD_REQUEST)
        elif instance.status != 11:
            return Response({'msg': '订单已被接走,换个订单看下吧'}, status=status.HTTP_400_BAD_REQUEST)

        # 设置接单者
        instance.receiver_user = request.user
        instance.receiver_confirm_time = timezone.now()

        # 根据是否要押金 设置订单状态
        if instance.deposit:
            # 需要押金
            instance.status = 12
            # 增加押金支付监控
            order_deposit_pay_timeout_monitor.apply_async(args=(instance.id,),
                                                          eta=datetime.utcnow() + timedelta(
                                                             seconds=settings.PAY_DEPOSIT_EXPIRE_TIME))
        else:
            # 不需要押金
            instance.status = 20
        instance.save()
        return Response({'msg': '接单成功'})

    @action(methods=['patch'], detail=True)
    def cancel(self, request, *args, **kwargs):
        # 取消订单
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({'msg': '订单不存在'}, status=status.HTTP_400_BAD_REQUEST)

        # 判断接单者是否是订单创建者
        # todo 佣兵取消订单
        if request.user is not instance.employer_user:
            return Response({'msg': '只有佣兵才能取消订单'}, status=status.HTTP_400_BAD_REQUEST)

        # 订单状态判断
        if instance.status < 0:
            return Response({'msg': '订单已被取消'}, status=status.HTTP_400_BAD_REQUEST)
        elif instance.status > 11:
            return Response({'msg': '订单正在进行中, 不能直接取消, 请联系客服'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif instance.status in [1, 2, 11]:
            # 还未接单  可以取消
            instance.status = -12
            instance.save()
            order_reward_pay_refund_monitor.apply_async(args=(instance.id, -12))
            return Response({'msg': '订单已被成功取消'})

    @action(methods=['patch'], detail=True)
    def complete(self, request, *args, **kwargs):
        # 订单确认完成
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({'msg': '订单不存在'}, status=status.HTTP_400_BAD_REQUEST)

        # 雇主确认完成
        if request.user is instance.employer_user:
            # 本来应该是改为22 雇主确认  现在直接更改为 订单已完成 50
            instance.status = 50
            instance.save()
        # 佣兵确认完成
        elif request.user is instance.receiver_user:
            instance.status = 21
            instance.save()
            # todo 监听两个小时之后设置订单已完成
        # todo 监听订单状态为50后的 1.佣兵账户余额增加;2.押金退回
        return Response({'msg': '确认成功'})
