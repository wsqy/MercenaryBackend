import xadmin
from .models import BalanceDetail, BankCard, WithDraw


class BalanceDetailAdmin:
    list_display = ['id', 'user', 'origin_type', 'order', 'balance', 'add_time']
    list_filter = ['user', 'origin_type', 'order']


class BankCardAdmin:
    list_display = ['card_no', 'user', 'name', 'phone', 'bank', 'id_card', 'add_time']
    list_filter = ['card_no', 'user', 'name']


class WithDrawAdmin:
    list_display = ['user', 'type', 'account', 'balance', 'status', 'add_time']
    list_filter = ['user', 'account']
    list_editable = ['status']
    ordering = ['add_time']


xadmin.site.register(BalanceDetail, BalanceDetailAdmin)
xadmin.site.register(BankCard, BankCardAdmin)
xadmin.site.register(WithDraw, WithDrawAdmin)
