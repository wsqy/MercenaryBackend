import xadmin
from .models import Company


class CompanyAdmin:
    list_display = ['name', 'telephone', 'address', 'weight', 'status']
    list_editable = ['weight', 'status']
    list_filter = ['name',]


xadmin.site.register(Company, CompanyAdmin)
