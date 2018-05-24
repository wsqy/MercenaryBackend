from django.db import models
from django.conf import settings
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


class BankCard(models.Model):
    """
    银行卡信息表
    """
    CARD_TYPE = (
        ('DC', '借记卡'),
        ('CC', '信用卡'),
        ('SCC', '贷记卡'),
        ('DCC', '存贷合一卡'),
        ('PC', '预付卡'),
        ('STPB', '标准存折'),
        ('STFA', '标准对公账户'),
        ('NSTFA', '非标准对公账户'),
    )
    user = models.ForeignKey(User, verbose_name='用户', help_text='用户')
    card_no = models.CharField(verbose_name='银行卡号', help_text='银行卡号',
                               max_length=64, unique=True)
    phone = models.CharField(max_length=11, blank=True, null=True,
                             verbose_name='手机号', help_text='手机号')
    name = models.CharField(max_length=10, blank=True, null=True,
                            verbose_name='姓名', help_text='真实姓名')
    id_card = models.CharField(verbose_name='身份证', help_text='身份证',
                               max_length=64, blank=True, null=True)
    card_type = models.CharField(verbose_name='银行卡类型', help_text='银行卡类型',
                                 max_length=8, blank=True, null=True,
                                 choices=CARD_TYPE)
    is_credit = models.BooleanField(verbose_name='是否是借记卡', default=True,
                                    help_text='是否是借记卡')
    bank = models.CharField(verbose_name='银行', help_text='银行',
                            max_length=2, blank=True, null=True,
                            choices=tuple(settings.CODE_TYPE.items()))
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间',
                                    help_text='添加时间')
    is_activate = models.BooleanField(verbose_name='是否激活', default=True,
                                      help_text='是否激活')

    class Meta:
        verbose_name = '银行卡表'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)

    def __str__(self):
        return self.card_no
