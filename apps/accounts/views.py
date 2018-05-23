from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from .models import BalanceDetail
from users.models import ProfileExtendInfo
from .serializers import BalanceSerializer, BalanceListSerializer

from utils.authentication import CommonAuthentication


class BalancesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class BalanceViewset(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = BalanceDetail.objects.all()
    authentication_classes = CommonAuthentication()
    pagination_class = BalancesPagination

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
