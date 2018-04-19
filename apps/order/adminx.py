import xadmin
from .models import SubCategory


class SubCategoryAdmin:
    list_display = ['name', 'classification', 'weight', 'is_active']
    search_fields = ['name', ]
    list_filter = ['classification', ]
    list_editable = ['name', 'classification', 'weight', 'is_active']


xadmin.site.register(SubCategory, SubCategoryAdmin)
