from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from .models import Classification, SubCategory
from .serializers import ClassificationSerializer, SubCategorySerializer


class ClassificationViewset(ListModelMixin, viewsets.GenericViewSet):
    queryset = Classification.objects.filter(is_active=True)
    serializer_class = ClassificationSerializer


class SubCategoryViewset(ListModelMixin, viewsets.GenericViewSet):
    queryset = SubCategory.objects.filter(is_active=True)
    serializer_class = SubCategorySerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('classification', )
