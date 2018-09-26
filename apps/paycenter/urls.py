from .views import PayOrderViewSet, PayReturnViewSet, PartTimePayOrderViewSet
from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

app_name = 'paycenter'

router = DefaultRouter()
router.register(r'paycenter', PayOrderViewSet, base_name='paycenter')
router.register(r'part-time', PartTimePayOrderViewSet, base_name='part-time')
router.register(r'return', PayReturnViewSet, base_name='pay_return')


urlpatterns = [
    # rest framework 的路由
    url(r'^', include(router.urls)),
]