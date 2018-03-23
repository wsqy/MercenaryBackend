from .views import DeviceRegisterViewset
from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

app_name = 'users'

router = DefaultRouter()
router.register(r'device', DeviceRegisterViewset, base_name="users")

urlpatterns = [
    # rest framework 的路由
    url(r'^', include(router.urls)),
]
