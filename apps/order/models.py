from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from utils.validators import IntRangeValidator
from area.models import District, School

User = get_user_model()


class SubCategory(models.Model):
    """
    订单小分类 订单暂不使用小分类
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
    CLASSIFICATION_CHOICE = (
        (1, '即时'),
        (2, '顺风'),
        (3, '替身'),
        (4, '技能'),
        (5, '活动'),
    )
    ORDER_STATUS = (
        # 任务发布前
        (1, '待付佣金'),
        (2, '佣金支付中'),
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
        (-21, '佣金支付超时取消'),
        (-22, '押金支付超时取消(不使用)'),
        (-23, '接单超时取消')
    )
    # 订单相关信息
    id = models.CharField(max_length=30, unique=True, verbose_name='订单号',
                          help_text='订单号', primary_key=True)
    status = models.SmallIntegerField(choices=ORDER_STATUS, default=1,
                                      verbose_name='订单状态', help_text='订单状态')
    # category = models.ForeignKey(SubCategory, verbose_name='分类', help_text='订单分类')
    category = models.PositiveSmallIntegerField(choices=CLASSIFICATION_CHOICE,
        default=1, verbose_name='所属分类', help_text='所属分类')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='订单创建时间',
                                       help_text='订单创建时间')
    complete_time = models.DateTimeField(null=True, help_text='订单完成时间',
                                         verbose_name='订单完成时间')
    detail = models.TextField(verbose_name='订单详细信息', help_text='订单详细信息', null=True)
    privacy = models.TextField(verbose_name='订单隐私信息', help_text='订单隐私信息', null=True)
    remark = models.TextField(verbose_name='订单备注信息', help_text='订单备注信息', null=True)
    detail = models.TextField(verbose_name='订单详细信息', help_text='订单详细信息', null=True)
    description = models.CharField(verbose_name='订单简短描述', help_text='订单简短描述',
                                   null=True, max_length=255)
    school = models.ForeignKey(School, verbose_name='学校', help_text='学院', blank=True, null=True)

    # 金额相关信息
    deposit = models.PositiveSmallIntegerField(default=0, verbose_name='押金',
                                               help_text='押金(分)')
    reward = models.PositiveSmallIntegerField(verbose_name='佣金', default=1,
                                              help_text='佣兵应得赏金(分)')
    pay_cost = models.PositiveSmallIntegerField(verbose_name='实付金额', default=1,
                                                help_text='雇主实付金额(分)')

    # 雇主相关信息
    employer_user = models.ForeignKey(User, verbose_name='雇主', help_text='雇主',
                                      related_name='employer_user')
    employer_receive_name = models.CharField(max_length=30, verbose_name='联系人姓名',
                                             help_text='联系人姓名', null=True)
    employer_receive_mobile = models.CharField(max_length=15, verbose_name='联系人手机号',
                                               help_text='联系人手机号', null=True)
    employer_complete_time = models.DateTimeField(null=True,
        verbose_name='雇主确认完成时间', help_text='雇主确认完成时间')

    # 接单相关信息
    receiver_user = models.ForeignKey(User, null=True, verbose_name='佣兵',
                                      help_text='佣兵', related_name='receiver_user')
    receiver_confirm_time = models.DateTimeField(null=True, verbose_name='佣兵接单时间',
                                                 help_text='佣兵接单时间')
    receiver_complete_time = models.DateTimeField(null=True,
        verbose_name='佣兵确认完成时间', help_text='佣兵确认完成时间')

    # 订单 从哪
    # from_addr_district = models.ForeignKey(District, verbose_name='订单开始的城市', null=True,
    #     help_text='订单开始的城市', related_name='from_district')
    from_addr_name = models.CharField(max_length=32, null=True, help_text='订单开始的点信息',
                                      verbose_name='订单开始的点信息')
    from_addr_detail = models.CharField(max_length=64, null=True, help_text='订单开始的具体地址',
                                        verbose_name='订单开始的具体地址')

    # 订单去哪
    # to_addr_district = models.ForeignKey(District, verbose_name='订单结束的城市', null=True,
    #     help_text='订单结束的城市', related_name='to_district')
    to_addr_name = models.CharField(max_length=128, null=True, help_text='订单结束的点信息',
                                    verbose_name='订单结束的点信息')
    to_addr_detail = models.CharField(max_length=128, null=True, help_text='订单结束的具体地址',
                                      verbose_name='订单结束的具体地址')
    # 订单的所在地信息
    create_district = models.ForeignKey(District, verbose_name='订单创建的城市', null=True,
        help_text='订单创建的城市', related_name='create_district')

    # 订单开始时间
    from_time = models.DateTimeField(null=True, verbose_name='订单开始时间',
                                     help_text='订单开始时间')
    # 订单结束时间
    to_time = models.DateTimeField(null=True, verbose_name='订单结束时间',
                                   help_text='订单结束时间')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)

    def __str__(self):
        return self.id


class OrderOperateLog(models.Model):
    """
    订单操作日志
    """
    order = models.ForeignKey(OrderInfo, verbose_name='订单', help_text='所属订单', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='操作用户', help_text='操作用户', null=True, blank=True)
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间', help_text='创建时间')
    message = models.TextField(verbose_name='操作日志', help_text='操作日志', null=True, blank=True)

    class Meta:
        verbose_name = '订单日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}-{}'.format(self.order, self.message)

    @classmethod
    def logging(cls_obj, order=None, user=None, message=''):
        try:
            cls_obj.objects.create(order=order, user=user, message=message)
        except:
            pass

