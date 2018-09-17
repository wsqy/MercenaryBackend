import xadmin
from .models import SubCategory, OrderInfo


class SubCategoryAdmin:
    list_display = ['name', 'classification', 'template', 'weight', 'is_active']
    search_fields = ['name', ]
    list_filter = ['classification', 'template']
    list_editable = ['name', 'classification', 'template', 'weight', 'is_active']


class OrderInfoAdmin:
    list_display = ['id', 'category', 'school', 'status', 'employer_user', 'receiver_user', 'description']
    list_filter = ['category', 'school', 'is_hot', 'status', 'employer_user', 'receiver_user']


xadmin.site.register(SubCategory, SubCategoryAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
