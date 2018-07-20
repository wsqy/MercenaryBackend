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


class RecruitOrder(models.Model):
    """
    招募令
    """
    OrderStatus = ()
    SignDeposit = (
        (0, '0元'),
        (500, '5元'),
        (1000, '10元'),
        (1500, '15元'),
        (2000, '20元')
    )
    name = models.CharField(blank=False, null=False, max_length=128, verbose_name='招募令标题', help_text='招募令标题')
    company = models.ForeignKey(Company, null=False, verbose_name='所属公司', help_text='所属公司')
    description = models.TextField(blank=True, null=True, verbose_name='任务描述', help_text='任务描述')
    requirement = models.TextField(blank=True, null=True, verbose_name='任务要求', help_text='任务要求')
    enrolment_max_num = models.PositiveSmallIntegerField(default=1, verbose_name='最大报名人数', help_text='最大报名人数')
    enrolment_min_num = models.PositiveSmallIntegerField(default=1, verbose_name='最少报名人数', help_text='最少报名人数')
    sign_start_time = models.DateTimeField(default=timezone.now, verbose_name='报名开始时间', help_text='报名开始时间')
    sign_end_time = models.DateTimeField(default=timezone.now, verbose_name='报名结束时间', help_text='报名结束时间')
    task_start_time = models.DateTimeField(default=timezone.now, verbose_name='任务开始时间', help_text='任务开始时间')
    task_end_time = models.DateTimeField(default=timezone.now, verbose_name='任务结束时间', help_text='任务结束时间')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间', help_text='创建时间')
    status = models.IntegerField(verbose_name='招募令状态', help_text='招募令状态', choices=OrderStatus, default=10)
    recruit_deposit = models.PositiveIntegerField(default=0, verbose_name='招募令押金', help_text='招募令押金(单位:分)')
    sign_deposit = models.PositiveIntegerField(default=0, choices=SignDeposit, verbose_name='报名所需押金', help_text='报名所需押金(单位:分)')
    weight = models.PositiveIntegerField(default=1, verbose_name='权重', help_text='权重')
    total_sign_num = models.PositiveSmallIntegerField(default=1, verbose_name='实际总报名人数', help_text='实际总报名人数')

    class Meta:
        verbose_name = '招募令表'
        verbose_name_plural = verbose_name
        ordering = ('-weight', '-create_time',)

    def __str__(self):
        return self.name


class RecruitCard(models.Model):
    """
    招募令卡片
    """
    recruit = models.ForeignKey(RecruitOrder, null=False, verbose_name='所属招募令', help_text='所属招募令')
    adress = models.ForeignKey(Address, null=False, verbose_name='任务地址', help_text='任务地址')
    sign_start_time = models.DateTimeField(default=timezone.now, verbose_name='报名开始时间', help_text='报名开始时间')
    sign_end_time = models.DateTimeField(default=timezone.now, verbose_name='报名结束时间', help_text='报名结束时间')
    task_start_time = models.DateTimeField(default=timezone.now, verbose_name='任务开始时间', help_text='任务开始时间')
    task_end_time = models.DateTimeField(default=timezone.now, verbose_name='任务结束时间', help_text='任务结束时间')
    min_num = models.PositiveSmallIntegerField(default=1, verbose_name='最小报名人数', help_text='最小报名人数')
    max_num = models.PositiveSmallIntegerField(default=1, verbose_name='最大报名人数', help_text='最大报名人数')
    sign_num = models.PositiveSmallIntegerField(default=1, verbose_name='实际报名人数', help_text='实际报名人数')
    status = models.IntegerField(verbose_name='状态', help_text='状态', default=0)
    wages = models.PositiveIntegerField(default=0, verbose_name='工资', help_text='工资')

    class Meta:
        verbose_name = '招募令卡片'
        verbose_name_plural = verbose_name
        ordering = ('-task_start_time',)

    def __str__(self):
        return '{}-{}'.format(self.recruit.name, self.task_start_time)
