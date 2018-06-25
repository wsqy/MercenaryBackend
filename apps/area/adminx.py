import xadmin

from .models import Province, City, District


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


xadmin.site.register(Province, ProvinceAdmin)
xadmin.site.register(City, CityAdmin)
xadmin.site.register(District, DistrictAdmin)
