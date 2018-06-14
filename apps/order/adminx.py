import xadmin
from .models import SubCategory, OrderInfo


class SubCategoryAdmin:
    list_display = ['name', 'classification', 'template', 'weight', 'is_active']
    search_fields = ['name', ]
    list_filter = ['classification', 'template']
    list_editable = ['name', 'classification', 'template', 'weight', 'is_active']


class OrderInfoAdmin:
    list_display = ['id', 'description', 'category', 'school', 'status']


xadmin.site.register(SubCategory, SubCategoryAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
