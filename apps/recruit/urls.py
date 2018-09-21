from recruit.views import CompanyViewset, PartTimeOrderViewset, PartTimeOrderCardViewset, PartTimeOrderSignViewset, PartTimeOrderCardSignViewset
from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

app_name = 'recruit'

router = DefaultRouter()
router.register(r'company', CompanyViewset, base_name='company')
router.register(r'part-time', PartTimeOrderViewset, base_name='part-time')
router.register(r'part-time-card', PartTimeOrderCardViewset, base_name='part-time-card')
router.register(r'part-time-sign', PartTimeOrderSignViewset, base_name='part-time-sign')
router.register(r'part-time-card-sign', PartTimeOrderCardSignViewset, base_name='part-time-card-sign')

urlpatterns = [
    # rest framework 的路由
    url(r'^', include(router.urls)),
]