import xadmin
from .models import BalanceDetail, BankCard


class BalanceDetailAdmin:
    list_display = ['id', 'user', 'origin_type', 'order', 'balance', 'add_time']
    list_filter = ['user', 'origin_type', 'order']


class BankCardAdmin:
    list_display = ['card_no', 'user', 'name', 'phone', 'bank', 'id_card', 'add_time']
    list_filter = ['card_no', 'user', 'name']


xadmin.site.register(BalanceDetail, BalanceDetailAdmin)
xadmin.site.register(BankCard, BankCardAdmin)


