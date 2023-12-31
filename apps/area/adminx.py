import xadmin

from .models import Province, City, District, School, Address


class ProvinceAdmin:
    list_display = ['id', 'name']
    search_fields = ['name', 'id']


class CityAdmin:
    list_display = ['id', 'name', 'province']
    search_fields = ['name', 'id']
    list_filter = ['province', ]


class DistrictAdmin:
    list_display = ['id', 'name', 'city']
    search_fields = ['name', 'id']
    list_filter = ['city__name', ]
    relfield_style = 'fk-ajax'


class SchoolAdmin:
    list_display = ['name', 'district', 'is_active']
    search_fields = ['name', 'district__name']
    list_filter = ['name', 'is_active']
    readonly_fields = ['geohash']
    open_bmap = True


class AddressAdmin:
    list_display = ['name', 'detail', 'district', 'weight', 'is_active', 'user']
    list_editable = ['weight', 'is_active', 'user']
    search_fields = ['name', 'district__name']
    list_filter = ['name', ]
    readonly_fields = ['geohash']
    open_bmap = True


xadmin.site.register(Province, ProvinceAdmin)
xadmin.site.register(City, CityAdmin)
xadmin.site.register(District, DistrictAdmin)
xadmin.site.register(School, SchoolAdmin)
xadmin.site.register(Address, AddressAdmin)