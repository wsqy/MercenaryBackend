import xadmin
from xadmin.plugins.actions import BaseActionView

from .models import BalanceDetail, BankCard, WithDraw, WithDrawDeal


class BalanceDetailAdmin:
    list_display = ['id', 'user', 'origin_type', 'order', 'balance', 'add_time']
    list_filter = ['user', 'origin_type', 'order']


class BankCardAdmin:
    list_display = ['card_no', 'user', 'name', 'phone', 'bank', 'id_card', 'add_time']
    list_filter = ['card_no', 'user', 'name']


class WithDrawAdmin:
    list_display = ['user', 'type', 'account', 'get_real_money', 'get_bank_name', 'status', 'add_time']
    list_filter = ['user', 'account', 'status']
    list_editable = ['status']
    ordering = ['add_time']


class UpdateDeal(BaseActionView):

    # 这里需要填写三个属性
    action_name = '批量更新为 已处理, 待银行打款'
    description = '批量更新为 已处理, 待银行打款'

    model_perm = 'change'

    # 而后实现 do_action 方法
    def do_action(self, queryset):
        queryset.update(status='20')


class UpdateSuccess(BaseActionView):

    # 这里需要填写三个属性
    action_name = '批量更新为 已完成'
    description = '批量更新为 已完成'

    model_perm = 'change'

    # 而后实现 do_action 方法
    def do_action(self, queryset):
        queryset.update(status='2')


class WithDrawDealAdmin:
    list_display = ['user', 'type', 'account', 'get_real_money', 'get_bank_name','status', 'add_time']
    list_filter = ['user', 'account', 'status']
    list_editable = ['status']
    ordering = ['add_time']
    actions = [UpdateDeal, UpdateSuccess]

    def queryset(self):
        qs = super(WithDrawDealAdmin, self).queryset()
        return qs.filter(status__in=['1', '20'])


xadmin.site.register(BalanceDetail, BalanceDetailAdmin)
xadmin.site.register(BankCard, BankCardAdmin)
xadmin.site.register(WithDraw, WithDrawAdmin)
xadmin.site.register(WithDrawDeal, WithDrawDealAdmin)
