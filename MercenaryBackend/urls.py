"""MercenaryBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import xadmin
from django.conf import settings
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import refresh_jwt_token

from users.views import DeviceRegisterViewset, SmsCodeViewset, UserViewset
from utils.views import get_celery_task_status
from area.views import DistrictViewset, SchoolViewSet
from order.views import OrderViewSet
# from order.views import SubCategoryViewset, OrderViewSet
from paycenter.views import PayOrderViewSet, PayReturnViewSet
from accounts.views import BalanceViewset, BankCardViewset
from resources.views import ResourceMaterialViewset
from recruit.views import CompanyViewset
router = DefaultRouter()

router.register(r'users', UserViewset, base_name='users')
router.register(r'devices', DeviceRegisterViewset, base_name='devices')
router.register(r'codes', SmsCodeViewset, base_name='codes')
router.register(r'district', DistrictViewset, base_name='district')
# router.register(r'category', SubCategoryViewset, base_name='category')
router.register(r'order', OrderViewSet, base_name='order')
router.register(r'paycenter', PayOrderViewSet, base_name='paycenter')
router.register(r'pay/return', PayReturnViewSet, base_name='pay_return')
router.register(r'balance', BalanceViewset, base_name='balance')
router.register(r'bank_card', BankCardViewset, base_name='bank_card')
router.register(r'resource', ResourceMaterialViewset, base_name='resource')
router.register(r'school', SchoolViewSet, base_name='school')
router.register(r'company', CompanyViewset, base_name='company')

urlpatterns = [
    url(r'^mercenary-admin/', xadmin.site.urls),
    # 刷新token
    url(r'^refresh_token/', refresh_jwt_token),
    # celery 查询任务状态
    url(r'^get_celery_task_status/$', get_celery_task_status),
    url(r'^', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        # 文档
        url(r'docs/', include_docs_urls(title='mercenary')),
    ]
