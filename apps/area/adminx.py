import xadmin
from .models import Province, City, Country


class ProvinceAdmin:
    list_display = ['id', 'name']
    search_fields = ['name', 'id']


class CityAdmin:
    list_display = ['id', 'name', 'province']
    search_fields = ['name', 'id']
    list_filter = ['province', ]


class CountryAdmin:
    list_display = ['id', 'name', 'city']
    search_fields = ['name', 'id']
    list_filter = ['city', ]


xadmin.site.register(Province, ProvinceAdmin)
xadmin.site.register(City, CityAdmin)
xadmin.site.register(Country, CountryAdmin)
