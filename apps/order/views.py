from django.conf import settings
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from .models import SubCategory, OrderInfo
from .serializers import SubCategorySerializer, OrderInfoCreateSerializer, OrderInfoListSerializer
from utils.common import generate_order_id
from utils.authentication import CommonAuthentication
from .cost import service_cost_calc
from .tasks import order_deposit_pay_timeout_monitor, order_reward_pay_timeout_monitor


class SubCategoryViewset(ListModelMixin, viewsets.GenericViewSet):
    queryset = SubCategory.objects.filter(is_active=True)
    serializer_class = SubCategorySerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('classification', )


class OrderViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = OrderInfo.objects.all()
    authentication_classes = CommonAuthentication()

    def get_permissions(self):
        if self.action in ['create', ]:
            return [permissions.IsAuthenticated()]
        return []

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderInfoCreateSerializer
        elif self.action == 'list':
            return OrderInfoListSerializer
        return OrderInfoListSerializer

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
        order_reward_pay_timeout_monitor.apply_async(args=[rec_dict['id']],
                                                     countdown=settings.PAY_DEFAULT_EXPIRE_TIME)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

