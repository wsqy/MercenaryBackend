from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from .models import SubCategory, OrderInfo
from .serializers import SubCategorySerializer, OrderInfoCreateSerializer, OrderInfoListSerializer


class SubCategoryViewset(ListModelMixin, viewsets.GenericViewSet):
    queryset = SubCategory.objects.filter(is_active=True)
    serializer_class = SubCategorySerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('classification', )


class OrderViewSet(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    queryset = OrderInfo.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderInfoCreateSerializer
        elif self.action == 'list':
            return OrderInfoListSerializer
        return OrderInfoListSerializer

