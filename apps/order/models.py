from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from utils.validators import IntRangeValidator

User = get_user_model()


class SubCategory(models.Model):
    """
    订单小分类
    """
    CLASSIFICATION_CHOICE = (
        (1, '即时'),
        (2, '顺风'),
        (3, '替身'),
        (4, '技能'),
        (5, '活动'),
    )
    TEMPLATE_CHOICE = (
        (1, '描述'),
        (2, '商品'),
        (3, '快递'),
    )
    name = models.CharField(max_length=255, null=False, verbose_name='分类名',
                            help_text='二级分类')
    weight = models.IntegerField(default=1, verbose_name='权重', help_text='权重',
                                 validators=IntRangeValidator())
    is_active = models.BooleanField(default=True, verbose_name='是否激活',
                                    help_text='是否激活')
    classification = models.PositiveSmallIntegerField(choices=CLASSIFICATION_CHOICE,
                                                      default=1, verbose_name='父分类',
                                                      help_text='所属分类')
    template = models.PositiveSmallIntegerField(choices=TEMPLATE_CHOICE, default=1,
                                                verbose_name='分类模板',
                                                help_text='分类数据所使用的模板')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['-weight']


class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        # 任务发布前
        (1, '待付赏金'),
        (2, '赏金支付中'),
        # 任务开始前
        (11, '待接单'),
        (12, '待付押金'),
        (13, '押金支付中'),
        # 完成相关
        (20, '任务进行中'),
        (21, '佣兵已确认'),
        (22, '雇主已确认'),
        # 评价
        (41, '待雇主评价(暂不使用)'),
        (42, '待佣兵评价(暂不使用)'),
        # 订单完成
        (50, '订单已完成'),
        # 申请取消
        (-11, '雇主申请取消'),
        (-12, '雇主主动取消'),
        (-13, '佣兵申请取消'),
        (-14, '佣兵主动取消'),
        (-15, '客服操作取消'),
        # 支付超时取消
        (-21, '赏金支付超时取消'),
        (-22, '押金支付超时取消'),
    )
    # 订单相关信息
    order_sn = models.CharField(max_length=30, unique=True, verbose_name='订单号',
                                help_text='订单号')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS, default=1,
                                            verbose_name="订单状态")
    category = models.ForeignKey(SubCategory, verbose_name='分类', help_text='订单分类')
    order_time = models.DateTimeField(default=timezone.now, verbose_name="订单创建时间",
                                      help_text='订单创建时间')
    order_time = models.DateTimeField(default=timezone.now, verbose_name='订单创建时间',
                                      help_text='订单创建时间')
    order_finish_time = models.DateTimeField(default=timezone.now,
                                             verbose_name='订单完成时间',
                                             help_text='订单完成时间')

    # 金额相关信息
    deposit = models.PositiveSmallIntegerField(verbose_name='押金', help_text='押金(分)', default=0)
    reward = models.PositiveSmallIntegerField(verbose_name='赏金', default=1,
                                              help_text='佣兵应得赏金(分)')
    pay_cost = models.PositiveSmallIntegerField(verbose_name='实付金额', default=1,
                                                help_text='雇主实付金额(分)')

    # 雇主相关信息
    employer_user = models.ForeignKey(User, verbose_name='雇主', help_text='雇主',
                                      related_name='employer_user')
    employer_receive_name = models.CharField(max_length=30, verbose_name='联系人姓名',
                                             help_text='联系人姓名')
    employer_receive_mobile = models.CharField(max_length=11, verbose_name='联系人手机号',
                                               help_text='联系人手机号')
    employer_complete_time = models.DateTimeField(null=True,
                                                  verbose_name='雇主确认完成时间',
                                                  help_text='雇主确认完成时间')

    # 接单相关信息
    receiver_user = models.ForeignKey(User, null=True, verbose_name='佣兵',
                                      help_text='佣兵', related_name='receiver_user')
    receiver_confirm_time = models.DateTimeField(null=True, verbose_name='佣兵接单时间',
                                                 help_text='佣兵接单时间')
    receiver_complete_time = models.DateTimeField(null=True,
                                                  verbose_name='佣兵确认完成时间',
                                                  help_text='佣兵确认完成时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)
