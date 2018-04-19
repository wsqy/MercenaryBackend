import xadmin
from .models import Classification, SubCategory


class ClassificationAdmin:
    list_display = ['name', 'weight', 'is_active']
    search_fields = ['name', ]
    list_editable = ['name', 'weight', 'is_active']


class SubCategoryAdmin:
    list_display = ['name', 'classification', 'weight', 'is_active']
    search_fields = ['name', ]
    list_filter = ['classification', ]
    list_editable = ['name', 'classification', 'weight', 'is_active']


xadmin.site.register(Classification, ClassificationAdmin)
xadmin.site.register(SubCategory, SubCategoryAdmin)
