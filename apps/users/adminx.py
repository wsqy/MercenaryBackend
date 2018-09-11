import xadmin
from xadmin.plugins.auth import UserAdmin
from django.contrib.auth import get_user_model

from .models import DeviceInfo, ProfileExtendInfo, ProfileInfo


User = get_user_model()


class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = "雇佣兵管理后台"
    site_footer = "mercenary"


class DeviceInfoAdmin:
    list_display = ['deviceid', 'model', 'device_ver', 'channel_code', 'date_joined']


class ProfileExtendInfoAdmin:
    list_display = ['balance', 'deposit_freeze', 'in_school']
    model = ProfileExtendInfo


class ProfileInfoAdmin(UserAdmin):
    list_display = ['id', 'username', 'nickname', 'first_name', 'date_joined']
    list_display_links = ['id', 'username']
    inlines = [ProfileExtendInfoAdmin, ]


# xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)

xadmin.site.unregister(User)
xadmin.site.register(User, ProfileInfoAdmin)
xadmin.site.register(DeviceInfo, DeviceInfoAdmin)

