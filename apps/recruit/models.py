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

    class Meta:
        verbose_name = '公司表'
        verbose_name_plural = verbose_name
        ordering = ('-weight', '-add_time')

    def __str__(self):
        return self.name


class CompanyLog(models.Model):
    company = models.ForeignKey(Company, verbose_name='公司', help_text='公司')
    user = models.ForeignKey(User, null=True, verbose_name='操作者', help_text='操作者')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间', help_text='创建时间')
    message = models.TextField(verbose_name='操作日志', help_text='操作日志', null=True, blank=True)

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
