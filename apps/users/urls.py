from rest_framework.routers import DefaultRouter

from .views import DeviceRegisterViewset, SmsCodeViewset

app_name = 'user'

router = DefaultRouter()
router.register(r'device', DeviceRegisterViewset, base_name="device")
router.register(r'code', SmsCodeViewset, base_name="code")


urlpatterns = router.urls
