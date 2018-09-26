from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from order.models import OrderInfo
from recruit.models import PartTimeOrderSignUp

User = get_user_model()


class PayOrder(models.Model):
    """
    支付订单
    """
    ORDER_TYPE = (
        (1, '押金'),
        (2, '加赏'),
        (3, '佣金'),
    )
    PAY_METHOD = (
        (1, '支付宝'),
        (2, '微信支付'),
        (3, '余额'),
    )
    STATUS = (
        (1, '未付款'),
        (2, '付款确认中'),
        (3, '已付款'),
        (4, '已退款'),
        (5, '支付超时'),
    )
    id = models.CharField(max_length=30, unique=True, verbose_name='支付订单编号',
                          help_text='支付订单编号', primary_key=True)
    order = models.ForeignKey(OrderInfo, verbose_name='所属订单', help_text='所属订单')
    user = models.ForeignKey(User, verbose_name='支付用户', help_text='支付用户')
    order_type = models.PositiveSmallIntegerField(choices=ORDER_TYPE,
                                                  verbose_name='支付类型',
                                                  help_text='支付类型')
    pay_method = models.PositiveSmallIntegerField(choices=PAY_METHOD,
                                                  verbose_name='支付方式',
                                                  help_text='支付方式')
    pay_cost = models.PositiveIntegerField(verbose_name='支付金额(分)',
                                           help_text='支付金额(分)')
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1,
                                              verbose_name='支付状态',
                                              help_text='支付状态')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='支付订单创建时间',
                                       help_text='支付创建时间')
    expire_time = models.DateTimeField(null=True,
                                       verbose_name='支付订单过期时间',
                                       help_text='支付订单过期时间')
    pay_time = models.DateTimeField(null=True, help_text='支付时间', verbose_name='支付时间')


class PartTimePayOrder(models.Model):
    """
    支付订单
    """
    ORDER_TYPE = (
        (1, '押金'),
        (2, '加赏'),
        (3, '佣金'),
    )
    PAY_METHOD = (
        (1, '支付宝'),
        (2, '微信支付'),
        (3, '余额'),
    )
    STATUS = (
        (1, '未支付'),
        (2, '支付中'),
        (3, '已支付'),
        (4, '已退款'),
        (5, '支付超时'),
    )
    id = models.CharField(max_length=30, unique=True, verbose_name='支付订单编号',
                          help_text='支付订单编号', primary_key=True)
    order = models.ForeignKey(PartTimeOrderSignUp, verbose_name='所属订单', help_text='所属订单')
    user = models.ForeignKey(User, verbose_name='支付用户', help_text='支付用户')
    order_type = models.PositiveSmallIntegerField(choices=ORDER_TYPE,
                                                  verbose_name='支付类型',
                                                  help_text='支付类型')
    pay_method = models.PositiveSmallIntegerField(choices=PAY_METHOD,
                                                  verbose_name='支付方式',
                                                  help_text='支付方式')
    pay_cost = models.PositiveIntegerField(verbose_name='支付金额(分)',
                                           help_text='支付金额(分)')
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1,
                                              verbose_name='支付状态',
                                              help_text='支付状态')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='支付订单创建时间',
                                       help_text='支付创建时间')
    expire_time = models.DateTimeField(null=True,
                                       verbose_name='支付订单过期时间',
                                       help_text='支付订单过期时间')
    pay_time = models.DateTimeField(null=True, help_text='支付时间', verbose_name='支付时间')
