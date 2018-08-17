from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from utils.validators import IntRangeValidator
from area.models import School

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
    description = models.TextField(verbose_name='订单详细信息', help_text='订单详细信息', null=True)
    privacy = models.TextField(verbose_name='订单隐私信息', help_text='订单隐私信息', null=True)
    school = models.ForeignKey(School, verbose_name='订单所在学校', help_text='订单所在学校', null=True)
    is_hot = models.BooleanField(verbose_name='热门订单', help_text='热门订单', default=False)

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

    # 任务地点
    from_addr = models.CharField(max_length=128, null=True, help_text='任务地点', verbose_name='任务地点')
    # 交付地点
    to_addr = models.CharField(max_length=128, null=True, help_text='交付地点', verbose_name='交付地点')

    # 任务开始时间
    from_time = models.DateTimeField(null=True, verbose_name='任务开始时间', help_text='任务开始时间')
    # 任务结束时间
    to_time = models.DateTimeField(null=True, verbose_name='任务结束时间', help_text='任务结束时间')

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
        except Exception as e:
            pass


class OrdersImage(models.Model):
    """
    订单图片
    """
    order = models.ForeignKey(OrderInfo, verbose_name='所属订单', help_text='所属订单', related_name='images')
    image = models.ImageField(upload_to='order/%Y/%m/%d', verbose_name='图片', help_text='图片', null=True, blank=True)
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间', help_text='添加时间')

    class Meta:
        verbose_name = '订单图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order.id


class OrderAdminCancel(models.Model):
    """
    订单管理取消表
    """
    TYPE = (
        ('1', '涉及非法内容'),
        ('2', '广告'),
        ('3', '色情暴力'),
        ('9', '其他'),
    )
    order = models.ForeignKey(OrderInfo, verbose_name='订单', help_text='所属订单', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='操作用户', help_text='操作用户', null=True, blank=True)
    category = models.CharField(choices=TYPE, max_length=2, null=True, blank=True, verbose_name='所属分类', help_text='所属分类')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间', help_text='创建时间')
    message = models.TextField(verbose_name='操作日志', help_text='操作日志', null=True, blank=True)

    class Meta:
        verbose_name = '订单管理取消表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}-{}'.format(self.order, self.message)
