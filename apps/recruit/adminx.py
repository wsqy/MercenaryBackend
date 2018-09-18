import xadmin
from .models import Company, PartTimeOrder


class CompanyAdmin:
    list_display = ['name', 'telephone', 'address', 'weight', 'status']
    list_editable = ['weight', 'status']
    list_filter = ['name',]


class PartTimeOrderAdmin:
    list_display = ['name', 'company', 'settlement_method', 'status', 'liaison']
    list_editable = ['status', 'liaison', 'settlement_method']
    list_filter = ['company', 'liaison', 'settlement_method']


xadmin.site.register(Company, CompanyAdmin)
xadmin.site.register(PartTimeOrder, PartTimeOrderAdmin)

