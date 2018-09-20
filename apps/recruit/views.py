from rest_framework import status
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Company, CompanyLog, PartTimeOrder, PartTimeOrderSignUp, PartTimeOrderCard, PartTimeOrderCardSignUp
from .serializers import (
    CompanyInfoSerializer, CompanyListSerializer, CompanyCreateSerializer,
    PartTimeOrderInfoSerializer, PartTimeOrderListSerializer, PartTimeOrderCreateSerializer,
    PartTimeOrderSignListSerializer, PartTimeOrderSignSerializer, PartTimeOrderSignCreateSerializer,
    PartTimeOrderCardSerializer
)
from .filters import PartTimeOrderFilter

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


class PartTimeOrderViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    """兼职招募令相关接口
    list:
        招募令列表
    retrieve:
        招募令详情
    create:
        新建招募令
    update:
        修改招募令信息
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
        return queryset

    @action(methods=['get'], detail=False)
    def publish(self, request, *args, **kwargs):
        # 我发布的招募令
        return self.list(request, *args, **kwargs)


class PartTimeOrderCardViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
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


class PartTimeOrderSignViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    """兼职招募令报名相关接口
    list:
        报名列表
    retrieve:
        报名详情
    create:
        报名
    update:
        修改报名信息
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
        _status = 2
        if recruit.deposit:
            _status = 1
            instance.status = 1
            instance.save()

        for card_data in cards_data:
            try:
                card = PartTimeOrderCard.objects.get(id=card_data)
                if card.recruit == recruit:
                    try:
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
