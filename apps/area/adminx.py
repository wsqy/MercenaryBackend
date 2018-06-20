import xadmin
from .models import Province, City, District, School


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
    list_filter = ['city', ]
    relfield_style = 'fk-ajax'


class SchoolAdmin:
    list_display = ['name', 'city', 'district']
    search_fields = ['name', 'city', 'district__name']
    list_filter = ['name', 'city', ]
    readonly_fields = ['geohash']


xadmin.site.register(Province, ProvinceAdmin)
xadmin.site.register(City, CityAdmin)
xadmin.site.register(District, DistrictAdmin)
xadmin.site.register(School, SchoolAdmin)