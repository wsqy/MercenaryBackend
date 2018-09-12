import logging
from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from django_filters.rest_framework import DjangoFilterBackend

from .models import SubCategory, OrderInfo, OrderOperateLog, OrdersImage, OrderAdminCancel
from .serializers import (
    SubCategorySerializer, OrderInfoSerializer, OrderInfoCreateSerializer,
    OrderInfoListSerializer, OrderInfoReceiptSerializer, OrderAdminCancelSerializer, OrderInfoUpdateSerializer
)
from utils.common import generate_order_id
from utils.authentication import CommonAuthentication
from utils.cost import service_cost_calc
from .tasks import (
    order_deposit_pay_timeout_monitor, order_reward_pay_timeout_monitor,
    order_reward_pay_refund_monitor, order_complete_monitor, order_deposit_pay_refund_monitor
)
from .filters import OrderFilter
from utils.pagination import CommonPagination

logger = logging.getLogger('order')


class SubCategoryViewset(ListModelMixin, viewsets.GenericViewSet):
    queryset = SubCategory.objects.filter(is_active=True)
    serializer_class = SubCategorySerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('classification', )


class OrderViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin,
                   UpdateModelMixin, viewsets.GenericViewSet):
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
    admin_list:
        学校管理员查看本校订单列表接口
    admin_cancel:
        管理员取消订单
    """
    authentication_classes = CommonAuthentication()
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, )
    # filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = OrderFilter
    # filter_fields = ('status', 'deposit')
    # ordering_fields = ('reward', )

    def get_permissions(self):
        if self.action in ['find', ]:
            return []
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderInfoCreateSerializer
        elif self.action == 'receipt':
            return OrderInfoReceiptSerializer
        elif self.action in ['find', 'release', 'service', 'admin_list']:
            return OrderInfoListSerializer
        elif self.action in ['retrieve',]:
            return OrderInfoSerializer
        elif self.action in ['admin_cancel',]:
            return OrderAdminCancelSerializer
        elif self.action in ['update',]:
            return OrderInfoUpdateSerializer

        return OrderInfoSerializer

    @staticmethod
    def get_order_info(instance):
        serializer = OrderInfoSerializer(instance)
        return serializer.data

    def create(self, request, *args, **kwargs):
        images_list = []
        for _im in request.data.getlist('images'):
            images_list.append({
                'image': _im
            })
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rec_dict = serializer.validated_data

        rec_dict['id'] = generate_order_id(order_type='10')
        if not rec_dict.get('employer_receive_name'):
            rec_dict['employer_receive_name'] = rec_dict['employer_user'].nickname
        if not rec_dict.get('employer_receive_mobile'):
            rec_dict['employer_receive_mobile'] = rec_dict['employer_user'].mobile
        rec_dict['reward'] = (rec_dict['pay_cost'] - service_cost_calc.service_calc(rec_dict['pay_cost']))

        order_obj = OrderInfo.objects.create(**rec_dict)
        for images in images_list:
            OrdersImage.objects.create(order=order_obj, **images)

        OrderOperateLog.logging(order=order_obj, user=self.request.user, message='新增订单')
        # 下单30分钟后查看订单佣金支付状态
        order_reward_pay_timeout_monitor.apply_async(args=(rec_dict['id'],),
                                                     countdown=settings.PAY_DEFAULT_EXPIRE_TIME)
        # 订单 to_time 到期 查询 订单是否未接,进行是否退押金步骤
        order_reward_pay_refund_monitor.apply_async(args=(rec_dict['id'], -23),
                                                    eta=(rec_dict['to_time'] - timezone.timedelta(hours=8)))
        return Response(serializer.data, status=status.HTTP_201_CREATED)



    def get_queryset(self):
        if self.action == 'release':
            queryset = OrderInfo.objects.filter(employer_user=self.request.user)
        elif self.action == 'service':
            queryset = OrderInfo.objects.filter(receiver_user=self.request.user)
        elif self.action == 'find':
            if self.request.query_params.get('is_hot'):
                queryset = OrderInfo.objects.filter(status=11)
            else:
                queryset = OrderInfo.objects.filter(status__in=[11, 50]).order_by('status', '-create_time')
        elif self.action == 'admin_list':
            queryset = OrderInfo.objects.filter(school=self.request.user.profileextendinfo.admin_school, status__gt=1)
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
        if request.user.id == instance.employer_user.id:
            return Response({'msg': '不能接自己的订单'}, status=status.HTTP_400_BAD_REQUEST)

        # 订单状态判断
        if instance.status < 0:
            return Response({'msg': '订单已被取消,换个订单看下吧'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif instance.status != 11:
            return Response({'msg': '订单已被接走,换个订单看下吧'},
                            status=status.HTTP_400_BAD_REQUEST)

        # 设置接单者
        instance.receiver_user = request.user
        instance.receiver_confirm_time = timezone.now()
        OrderOperateLog.logging(order=instance, user=self.request.user, message='接单')

        # 根据是否要押金 设置订单状态
        if instance.deposit:
            # 需要押金
            instance.status = 12
            # 增加押金支付监控
            order_deposit_pay_timeout_monitor.apply_async(args=(instance.id,),
                                                          countdown=settings.PAY_DEPOSIT_EXPIRE_TIME)
        else:
            # 不需要押金
            instance.status = 20
        instance.save()
        return Response({'msg': '接单成功'})

    @action(methods=['patch'], detail=True)
    def cancel(self, request, *args, **kwargs):
        # 取消订单
        instance = self.get_object()
        if request.user == instance.employer_user:
            logger.info('当前申请取消者是雇主')
            # 订单状态判断
            if instance.status < 0:
                logger.info('订单已被取消')
                return Response({'msg': '订单已被取消'}, status=status.HTTP_400_BAD_REQUEST)
            elif instance.status > 11:
                if instance.receiver_confirm_time and (timezone.now() - instance.receiver_confirm_time).total_seconds() < settings.ORDER_RUNNING_CANCEL_TIME:
                    # 满足雇主取消订单条件
                    order_reward_pay_refund_monitor.apply_async(args=(instance.id, -12))
                    order_deposit_pay_refund_monitor.apply_async(args=(instance.id,))
                    OrderOperateLog.logging(order=instance, user=request.user, message='雇主主动取消订单')
                    return Response({'msg': '雇主申请取消订单成功'}, status=status.HTTP_200_OK)
                return Response({'msg': '订单正在进行中, 不能直接取消, 请联系客服'},
                                status=status.HTTP_400_BAD_REQUEST)
            elif instance.status in [1, 2, 11]:
                # 还未接单  可以取消
                logger.info('准备进行退款操作')
                OrderOperateLog.logging(order=instance, user=self.request.user, message='雇主主动取消订单')
                order_reward_pay_refund_monitor.apply_async(args=(instance.id, -12))
                return Response({'msg': '订单已被成功取消'})
        else:
            logger.info('当前申请取消者是佣兵')
            if instance.receiver_confirm_time and (timezone.now() - instance.receiver_confirm_time).total_seconds() < settings.ORDER_RUNNING_CANCEL_TIME:
                # 满足雇主取消订单条件
                order_deposit_pay_refund_monitor.apply_async(args=(instance.id,))
                OrderOperateLog.logging(order=instance, user=request.user, message='佣兵取消订单')
                instance.status = 11
                instance.receiver_confirm_time = None
                instance.receiver_user = None
                instance.save()
                return Response({'msg': '佣兵申请取消订单成功'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': '订单正在进行中, 不能直接取消, 请联系客服'}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['patch'], detail=True)
    def complete(self, request, *args, **kwargs):
        # 订单确认完成
        try:
            instance = self.get_object()
        except Exception as e:
            return Response({'msg': '订单不存在'}, status=status.HTTP_400_BAD_REQUEST)

        # 雇主确认完成
        if request.user == instance.employer_user:
            # 本来应该是改为22 雇主确认  现在直接更改为 订单已完成 50
            if instance.status in (20,21):
                instance.status = 50
                instance.complete_time = timezone.now()
                instance.employer_complete_time = timezone.now()
                instance.save()
                OrderOperateLog.logging(order=instance, user=self.request.user, message='雇主点击完成')
            else:
                return Response({'msg': '确认失败,当前订单状态: {}'.format(instance.get_status_display())}, status=status.HTTP_400_BAD_REQUEST)
        # 佣兵确认完成
        elif request.user == instance.receiver_user:
            if instance.status in (20, ):
                instance.status = 21
                instance.receiver_complete_time = timezone.now()
                instance.save()
                OrderOperateLog.logging(order=instance, user=self.request.user, message='佣兵点击完成')
                order_complete_monitor.apply_async(args=(instance.id,),
                                                   countdown=settings.PAY_COMPLETE_EXPIRE_TIME)
            else:
                return Response({'msg': '确认失败,当前订单状态: {}'.format(instance.get_status_display())}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'msg': '确认成功'})

    @action(methods=['get'], detail=False)
    def admin_list(self, request, *args, **kwargs):
        # 我发布的订单
        return self.list(request, *args, **kwargs)


    @action(methods=['get'], detail=False)
    def admin_cancel_type(self, request, *args, **kwargs):
        # 管理员取消订单分类列表
        return Response(dict(OrderAdminCancel.TYPE), status=status.HTTP_200_OK)


    @action(methods=['post'], detail=False)
    def admin_cancel(self, request, *args, **kwargs):
        # 管理员取消订单
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('order').status < 0:
            return Response({'msg': '订单已为取消状态'}, status=status.HTTP_400_BAD_REQUEST)
        elif serializer.validated_data.get('order').status >= 50:
            return Response({'msg': '订单已完成,不能取消，请联系管理员'}, status=status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()
        order_reward_pay_refund_monitor.apply_async(args=(instance.order.id, -15))
        order_deposit_pay_refund_monitor.apply_async(args=(instance.order.id,))
        OrderOperateLog.logging(order=instance.order, user=request.user, message='管理员取消')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
