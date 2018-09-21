from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from area.models import Address


User = get_user_model()


class Company(models.Model):
    """
    认证公司表
    """
    COMPANY_STATUS = (
        (10, '待认证'),
        (20, '认证中'),
        (30, '认证完成'),
        (50, '认证失败'),
    )
    name = models.CharField(blank=False, null=False, max_length=128,
                            verbose_name='公司名称', help_text='公司名称')
    user = models.ForeignKey(User, null=True, verbose_name='操作者', help_text='操作者')
    telephone = models.CharField(blank=True, null=True, max_length=20,
                                 verbose_name='公司联系方式', help_text='公司联系方式')
    address = models.ForeignKey(Address, null=True,
                                verbose_name='公司地址', help_text='公司地址')
    introduce = models.TextField(blank=True, null=True, verbose_name='公司介绍',
                                 help_text='公司介绍')
    logo = models.ImageField(blank=True, null=True, verbose_name='企业logo',
                             upload_to='company/logo',
                             help_text='企业logo 现阶段是阿里云OSS地址')
    weight = models.IntegerField(default=1, verbose_name='权重',help_text='权重')
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间',
                                    help_text='添加时间')
    status = models.IntegerField(verbose_name='认证状态', help_text='认证状态',
                                 choices=COMPANY_STATUS, default=10)
    remark = models.TextField(blank=True, null=True, verbose_name='申请备注',
                              help_text='公司认证申请备注信息')

    class Meta:
        verbose_name = '公司表'
        verbose_name_plural = verbose_name
        ordering = ('-weight', '-add_time')

    def __str__(self):
        return self.name


class CompanyLog(models.Model):
    """
    企业认证申请日志(暂未使用)
    """
    company = models.ForeignKey(Company, verbose_name='公司', help_text='公司')
    user = models.ForeignKey(User, null=True, verbose_name='操作者', help_text='操作者')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间',
                                       help_text='创建时间')
    message = models.TextField(null=True, blank=True, verbose_name='操作日志',
                               help_text='操作日志')

    @classmethod
    def logging(cls_obj, company, user=None, message=''):
        try:
            cls_obj.objects.create(company=company, user=user, message=message)
        except:
            pass

    class Meta:
        verbose_name = '公司认证日志表'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)

    def __str__(self):
        return self.message


class PartTimeOrder(models.Model):
    """
    招募令 兼职
    """
    SettlementMethodChoices = (
        ('1', '日结'),
        ('2', '月结'),
    )
    OrderStatus = (
        (10, '待审核'),
        (20, '进行中'),
        (30, '已完成'),
        (-10, '审核未通过'),
        (-20, '商户取消'),
    )
    name = models.CharField(max_length=32, verbose_name='招募令标题', help_text='招募令标题')
    company = models.ForeignKey(Company, verbose_name='所属公司', help_text='所属公司')
    description = models.TextField(blank=True, null=True, verbose_name='任务描述', help_text='任务描述')
    requirement = models.TextField(blank=True, null=True, verbose_name='任务要求', help_text='任务要求')
    wages = models.PositiveIntegerField(default=0, verbose_name='佣金/小时(单位:分)', help_text='佣金/小时(单位:分)')
    settlement_method = models.CharField(max_length=2, verbose_name='结算方式', help_text='结算方式', choices=SettlementMethodChoices, default='1')
    deposit = models.PositiveIntegerField(default=0, verbose_name='招募令押金(单位:分)', help_text='招募令押金(单位:分)')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='报名截止时间', help_text='报名截止时间')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间', help_text='创建时间')
    status = models.IntegerField(verbose_name='招募令状态', help_text='招募令状态', choices=OrderStatus, default=10)
    weight = models.PositiveIntegerField(default=1, verbose_name='权重', help_text='权重')
    enrol_total = models.PositiveIntegerField(default=0, verbose_name='报名人数', help_text='报名人数')
    liaison = models.ForeignKey(User, blank=True, null=True, verbose_name='对接负责人', help_text='对接负责人')
    address_info = models.CharField(max_length=128, verbose_name='任务地址信息', help_text='任务地址信息', default='多地址可选')
    cust_username = models.CharField(max_length=8, verbose_name='招募令联系人姓名', help_text='招募令联系人姓名', blank=True, null=True)
    cust_mobile = models.CharField(max_length=15, verbose_name='招募令联系人电话', help_text='招募令联系人电话', blank=True, null=True)

    class Meta:
        verbose_name = '兼职招募令表'
        verbose_name_plural = verbose_name
        ordering = ('-weight', '-create_time',)

    def __str__(self):
        return '{}招聘{}'.format(self.company.name, self.name)


class PartTimeOrderCard(models.Model):
    """
    兼职卡片
    """
    CardStatus = (
        (10, '报名未开始'),
        (20, '报名中'),
        (30, '任务未开始'),
        (40, '进行中'),
        (50, '结算中'),
        (60, '已完成'),
        (-10, '商户取消'),
    )
    recruit = models.ForeignKey(PartTimeOrder, verbose_name='所属招募令', help_text='所属招募令', related_name='cards')
    address = models.ForeignKey(Address, verbose_name='任务地址', help_text='任务地址')
    start_time = models.DateTimeField(verbose_name='任务开始时间', help_text='任务开始时间')
    end_time = models.DateTimeField(verbose_name='任务结束时间', help_text='任务结束时间')
    registration_deadline_time = models.DateTimeField(blank=True, null=True, verbose_name='报名截止时间', help_text='报名截止时间')
    work_time = models.FloatField(default=0, verbose_name='工作时长', help_text='工作时长')
    reward = models.PositiveIntegerField(default=0, verbose_name='预计佣金', help_text='预计佣金')
    enrol_total = models.PositiveIntegerField(default=0, verbose_name='报名人数', help_text='报名人数')
    enrol_count = models.PositiveIntegerField(default=0, verbose_name='需要人数', help_text='需要人数')
    status = models.IntegerField(verbose_name='状态', help_text='状态', default=10, choices=CardStatus)

    def save(self, *args, **kwargs):
        """
        保存时自动计算佣金
        """
        if not self.work_time:
            self.work_time = round((self.end_time-self.start_time).seconds / 3600, 1)
        if not self.reward:
            self.reward = int(self.work_time * self.recruit.wages)
        super(PartTimeOrderCard, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '兼职卡片'
        verbose_name_plural = verbose_name
        ordering = ('start_time',)

    def __str__(self):
        return '{}-{}'.format(self.recruit.name, self.start_time)


class PartTimeOrderSignUp(models.Model):
    """
    兼职报名表
    """
    SignStatus = (
        (1, '押金支付中'),
        (11, '任务进行中'),
        (30, '已完成'),
        (-1, '押金支付超时取消'),
        (-10, '商户取消'),
        (-20, '用户取消'),
    )
    user = models.ForeignKey(User, verbose_name='报名用户', help_text='报名用户')
    recruit = models.ForeignKey(PartTimeOrder, verbose_name='所属招募令', help_text='所属招募令', related_name='recruits')
    status = models.IntegerField(verbose_name='状态', help_text='状态', default=1, choices=SignStatus)
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间', help_text='创建时间')
    cust_username = models.CharField(max_length=8, verbose_name='联系人姓名', help_text='联系人姓名', blank=True, null=True)
    cust_mobile = models.CharField(max_length=15, verbose_name='联系人电话', help_text='联系人电话', blank=True, null=True)
    cust_sex = models.BooleanField(verbose_name='联系人性别', help_text='联系性别', default=True)

    class Meta:
        verbose_name = '兼职报名表'
        verbose_name_plural = verbose_name
        ordering = ('create_time',)
        unique_together = (('user', 'recruit'),)

    def __str__(self):
        return '{} 报名了 {}'.format(self.user, self.recruit)


class PartTimeOrderCardSignUp(models.Model):
    """
    兼职卡片报名表
    """
    SignStatus = (
        (1, '押金支付中'),
        (2, '商户审核中'),
        (11, '任务进行中'),
        (30, '已完成'),
        (-1, '押金支付超时取消'),
        (-10, '商户取消'),
        (-20, '用户取消'),
    )
    user = models.ForeignKey(User, verbose_name='报名用户', help_text='报名用户')
    recruit = models.ForeignKey(PartTimeOrder, verbose_name='所属招募令', help_text='所属招募令', related_name='card_recruits')
    sign = models.ForeignKey(PartTimeOrderSignUp, verbose_name='所属报名', help_text='所属报名', related_name='signs')
    card = models.ForeignKey(PartTimeOrderCard, verbose_name='所属卡片', help_text='所属卡片', related_name='cards')
    status = models.IntegerField(verbose_name='状态', help_text='状态', default=1, choices=SignStatus)
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间', help_text='创建时间')
    reward = models.PositiveIntegerField(default=0, verbose_name='佣金', help_text='佣金')

    def save(self, *args, **kwargs):
        """
        保存时自动计算佣金
        """
        if not self.reward:
            self.reward = self.card.reward
            super(PartTimeOrderCardSignUp, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '兼职卡片报名表'
        verbose_name_plural = verbose_name
        ordering = ('create_time',)
        unique_together = (('user', 'card'),)

    def __str__(self):
        return '{} 报名了 {}'.format(self.user, self.card)


