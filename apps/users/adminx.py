import xadmin
from .models import DeviceInfo


class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = "雇佣兵管理后台"
    site_footer = "mercenary"


class DeviceInfoAdmin:
    list_display = ['deviceid', 'model', 'device_ver', 'channel_code', 'date_joined']


# xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(DeviceInfo, DeviceInfoAdmin)