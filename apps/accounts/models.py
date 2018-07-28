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
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间',
                                    help_text='添加时间')

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

    user = models.ForeignKey(User, verbose_name='用户', help_text='用户')
    card_no = models.CharField(verbose_name='银行卡号', help_text='银行卡号',
                               max_length=64, unique=True)
    phone = models.CharField(max_length=11, blank=True, null=True,
                             verbose_name='手机号', help_text='手机号')
    name = models.CharField(max_length=10, blank=True, null=True,
                            verbose_name='姓名', help_text='真实姓名')
    id_card = models.CharField(verbose_name='身份证', help_text='身份证', max_length=64)
    card_type = models.CharField(verbose_name='银行卡类型', help_text='银行卡类型',
                                 max_length=8, blank=True, null=True,
                                 choices=tuple(settings.BANK_CARD_TYPE.items()))
    is_credit = models.BooleanField(verbose_name='是否是借记卡', default=True,
                                    help_text='是否是借记卡')
    bank = models.CharField(verbose_name='银行', help_text='银行',
                            max_length=20, blank=True, null=True,
                            choices=tuple(settings.BANK_CARD.items()))
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


class WithDraw(models.Model):
    """
    提现信息表
    """
    ORIGIN_TYPE = (
        ('1', '银行卡'),
    )
    STATUS = (
        ('1', '待处理'),
        ('2', '提现完成'),
        ('3', '提现异常'),
    )

    user = models.ForeignKey(User, verbose_name='用户', help_text='用户')
    type = models.CharField(verbose_name='提现去向', help_text='提现去向',
                            max_length=2, choices=ORIGIN_TYPE, default='1')
    account = models.CharField(verbose_name='提现账号', help_text='提现账号',
                               max_length=64, blank=True, null=True)
    balance = models.IntegerField(default=0, verbose_name='金额', help_text='提现金额(分)')
    status = models.CharField(verbose_name='状态', help_text='提现状态',
                              max_length=1, choices=STATUS, default='1')
    remark = models.CharField(verbose_name='备注信息', blank=True, null=True,
                              help_text='备注信息', max_length=128)
    add_time = models.DateTimeField(default=timezone.now, verbose_name='申请时间',
                                    help_text='申请时间')

    class Meta:
        verbose_name = '提现信息表'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)

    def __str__(self):
        return '{}申请提现{}分到{}'.format(self.user.nickname, self.balance, self.account)


class WithDrawDeal(WithDraw):
    class Meta:
        verbose_name = '待处理提现'
        verbose_name_plural = verbose_name
        proxy = True
