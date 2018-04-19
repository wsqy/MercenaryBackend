import xadmin
from .models import SubCategory


class SubCategoryAdmin:
    list_display = ['name', 'classification', 'template', 'weight', 'is_active']
    search_fields = ['name', ]
    list_filter = ['classification', 'template']
    list_editable = ['name', 'classification', 'template', 'weight', 'is_active']


xadmin.site.register(SubCategory, SubCategoryAdmin)
