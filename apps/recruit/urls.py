from recruit.views import CompanyViewset, PartTimeOrderViewset, PartTimeOrderCardViewset
from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

app_name = 'recruit'

router = DefaultRouter()
router.register(r'company', CompanyViewset, base_name='company')
router.register(r'part-time', PartTimeOrderViewset, base_name='part-time')
router.register(r'part-time-card', PartTimeOrderCardViewset, base_name='part-time-card')


urlpatterns = [
    # rest framework 的路由
    url(r'^', include(router.urls)),
]