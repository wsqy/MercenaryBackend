import xadmin
from .models import BalanceDetail


class BalanceDetailAdmin:
    list_display = ['id', 'user', 'origin_type', 'order', 'balance', 'remark']
    list_filter = ['user', 'origin_type', 'order']


xadmin.site.register(BalanceDetail, BalanceDetailAdmin)

