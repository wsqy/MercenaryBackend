import xadmin
from .models import DeviceInfo, ProfileExtendInfo, School, Address


class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = "雇佣兵管理后台"
    site_footer = "mercenary"


class DeviceInfoAdmin:
    list_display = ['deviceid', 'model', 'device_ver', 'channel_code', 'date_joined']


class ProfileExtendInfoAdmin:
    list_display = ['user', 'balance', 'deposit_freeze', 'in_school', 'admin_school']


class SchoolAdmin:
    list_display = ['name', 'district']
    search_fields = ['name', 'district__name']
    list_filter = ['name', ]
    readonly_fields = ['geohash']
    open_bmap = True


class AddressAdmin:
    list_display = ['name', 'detail', 'district', 'weight', 'is_active', 'user']
    list_editable = ['weight', 'is_active', 'user']
    search_fields = ['name', 'district__name']
    list_filter = ['name', ]
    readonly_fields = ['geohash']
    open_bmap = True


# xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(DeviceInfo, DeviceInfoAdmin)
xadmin.site.register(ProfileExtendInfo, ProfileExtendInfoAdmin)
xadmin.site.register(School, SchoolAdmin)
xadmin.site.register(Address, AddressAdmin)
