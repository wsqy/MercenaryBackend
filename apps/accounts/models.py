from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class BalanceDetail(models.Model):
    """
    账户余额详情
    """
    ORIGIN_TYPE_CHOICE = (
        ('10', '跑腿单佣金'),
        ('20', '招募令佣金'),
        ('30', '提现'),
    )

    user = models.ForeignKey(User, verbose_name='用户', help_text='用户')

    origin_type = models.CharField(verbose_name='变动类型', help_text='变动类型',
                                   max_length=5, choices=ORIGIN_TYPE_CHOICE)

    order = models.CharField(verbose_name='来源订单', help_text='来源订单',
                             max_length=30, blank=True, null=True)

    balance = models.IntegerField(default=0, verbose_name='金额',
                                  help_text='变动金额(分)')

    remark = models.CharField(verbose_name='备注信息', blank=True, null=True,
                              help_text='备注信息', max_length=128)
    add_time = models.DateTimeField(default=timezone.now, verbose_name='时间',
                                    help_text='时间')

    class Meta:
        verbose_name = '账户余额变动表'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)

    def __str__(self):
        return '{}-{}'.format(self.get_origin_type_display(), self.balance)

