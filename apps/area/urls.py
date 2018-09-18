from .views import ProvinceViewset, DistrictViewset, CityViewset, SchoolViewSet, AddressViewSet
from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

app_name = 'area'

router = DefaultRouter()
router.register(r'province', ProvinceViewset, base_name='province')
router.register(r'district', DistrictViewset, base_name='district')
router.register(r'city', CityViewset, base_name='city')
router.register(r'school', SchoolViewSet, base_name='school')
router.register(r'address', AddressViewSet, base_name='address')


urlpatterns = [
    # rest framework 的路由
    url(r'^', include(router.urls)),
]