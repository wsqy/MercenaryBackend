from django.utils import timezone
from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Company, CompanyLog, PartTimeOrder, PartTimeOrderSignUp, PartTimeOrderCard, PartTimeOrderCardSignUp
from .serializers import (
    CompanyInfoSerializer, CompanyListSerializer, CompanyCreateSerializer,
    PartTimeOrderInfoSerializer, PartTimeOrderListSerializer, PartTimeOrderCreateSerializer,
    PartTimeOrderSignListSerializer, PartTimeOrderSignSerializer, PartTimeOrderSignCreateSerializer,
    PartTimeOrderSignInfoSerializer, PartTimeOrderCardSerializer, PartTimeOrderCardSignCreateSerializer
)
from .filters import PartTimeOrderFilter
from .tasks import check_order_signup_status

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


class PartTimeOrderViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    """兼职招募令相关接口
    list:
        招募令列表
    retrieve:
        招募令详情
    create:
        新建招募令
    update:
        修改招募令信息
    publish:
        显示我发布的招募令(适用于企业的订单管理页面)
    """
    queryset = PartTimeOrder.objects.all()
    pagination_class = CommonPagination
    authentication_classes = CommonAuthentication()

    filter_backends = (DjangoFilterBackend,)
    filter_class = PartTimeOrderFilter

    def get_serializer_class(self):
        if self.action in ['list', 'publish']:
            return PartTimeOrderListSerializer
        elif self.action == 'create':
            return PartTimeOrderCreateSerializer
        return PartTimeOrderInfoSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'publish':
            queryset = queryset.filter(company=self.request.user.profileextendinfo.admin_company)
        elif self.action == 'list':
            queryset = queryset.filter(status=20)
            queryset = queryset.filter(Q(end_time__gt=timezone.now()) | Q(end_time__isnull=True))
        return queryset

    @action(methods=['get'], detail=False)
    def publish(self, request, *args, **kwargs):
        # 我发布的招募令
        return self.list(request, *args, **kwargs)


class PartTimeOrderCardViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
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


class PartTimeOrderSignViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    """兼职招募令报名相关接口
    list:
        报名列表
    retrieve:
        报名详情
    create:
        报名
    mine:
        我报名的招募令
    """
    queryset = PartTimeOrderSignUp.objects.all()
    pagination_class = CommonPagination
    authentication_classes = CommonAuthentication()

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'mine':
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return PartTimeOrderSignCreateSerializer
        elif self.action in ['list', 'mine']:
            return PartTimeOrderSignListSerializer
        elif self.action == 'retrieve':
            return PartTimeOrderSignInfoSerializer
        return PartTimeOrderSignSerializer

    @action(methods=['get'], detail=False)
    def mine(self, request, *args, **kwargs):
        # 我报名的招募令
        return self.list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'msg:' '不得查看他人的报名信息'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        # 招募令报名
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cards_data = serializer.validated_data.get('cards')
        try:
            recruit_id = request.data.get('recruit')
            recruit = PartTimeOrder.objects.get(id=recruit_id)
        except Exception as e:
            return Response({'msg': '所选招募令不存在'}, status=status.HTTP_400_BAD_REQUEST)
        _user = serializer.validated_data.get('user')
        try:
            instance = PartTimeOrderSignUp.objects.create(user=_user, recruit=recruit)
        except Exception as e:
            return Response({'msg': '已报名此招募令'}, status=status.HTTP_400_BAD_REQUEST)
        recruit.enrol_total += 1
        recruit.save()
        if not recruit.deposit:
            instance.status = 11
            instance.save()

        for card_data in cards_data:
            try:
                card = PartTimeOrderCard.objects.get(id=card_data)
                if card.recruit == recruit:
                    if card.registration_deadline_time and card.registration_deadline_time < timezone.now():
                        return Response({'msg': '该卡片已经停止报名'}, status=status.HTTP_400_BAD_REQUEST)
                    try:
                        _status = 1
                        if instance.status == 11:
                            _status = 2
                        PartTimeOrderCardSignUp.objects.create(sign=instance, user=_user, card=card, recruit=recruit, status=_status)
                        card.enrol_total += 1
                        card.save()
                    except Exception as e:
                        return Response({'msg': '已报名此招募令卡片'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'msg': '所选卡片:{}不属于招募令:{}'.format(card_data, recruit.name)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'msg': '所选卡片:{}不存在'.format(card_data)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': '报名成功'}, status=status.HTTP_201_CREATED)


class PartTimeOrderCardSignViewset(CreateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    """兼职招募令卡片报名相关接口
    create:
        为招募令报名新增卡片
    destroy:
        取消报名
    """
    serializer_class = PartTimeOrderCardSignCreateSerializer
    authentication_classes = CommonAuthentication()
    queryset = PartTimeOrderCardSignUp.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        # 根据招募令报名状态确定卡片报名状态
        if instance.sign.status == 1:
            instance.status = 1
        else:
            instance.status = 2
        instance.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        sign = instance.sign
        recruit = instance.recruit
        card = instance.card

        # 检查报名所属的卡片是否属于招募令
        if instance.user != request.user:
            return Response({'msg': '所选报名非法: 不是本人的报名'}, status=status.HTTP_400_BAD_REQUEST)

        if card.registration_deadline_time:
            if card.registration_deadline_time < timezone.now():
                return Response({'msg': '截止时间已到, 不能取消.如要取消请联系客服'}, status=status.HTTP_400_BAD_REQUEST)
        elif card.start_time and card.start_time < timezone.now():
            return Response({'msg': '任务时间已到, 不能取消.如要取消请联系客服'}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        check_order_signup_status.apply_async(args=(sign.id, -20, '兼职招募令报名取消退款'))

        return Response({'msg': '取消报名成功'}, status=status.HTTP_204_NO_CONTENT)
