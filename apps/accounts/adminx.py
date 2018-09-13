import xadmin
from .models import BalanceDetail, BankCard, WithDraw, WithDrawDeal


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


class WithDrawDealAdmin:
    list_display = ['user', 'type', 'account', 'get_real_money', 'status', 'add_time']
    list_filter = ['user', 'account']
    list_editable = ['status']
    ordering = ['add_time']

    def queryset(self):
        qs = super(WithDrawDealAdmin, self).queryset()
        return qs.filter(status='1')


xadmin.site.register(BalanceDetail, BalanceDetailAdmin)
xadmin.site.register(BankCard, BankCardAdmin)
xadmin.site.register(WithDraw, WithDrawAdmin)
xadmin.site.register(WithDrawDeal, WithDrawDealAdmin)
