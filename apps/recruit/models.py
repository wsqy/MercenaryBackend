from django.db import models
from django.utils import timezone

from area.models import Address


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
    address = models.ForeignKey(Address, blank=True, null=True,
                                verbose_name='公司地址', help_text='公司地址')
    introduce = models.TextField(blank=True, null=True, verbose_name='公司介绍',
                                 help_text='公司介绍')
    logo = models.ImageField(blank=True, null=True, verbose_name='企业logo',
                             upload_to='company/logo',
                             help_text='企业logo 现阶段是阿里云OSS地址')
    weight = models.IntegerField(default=1, verbose_name='权重')
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间',
                                    help_text='添加时间')
    status = models.IntegerField(verbose_name='认证状态', help_text='认证状态',
                                 choices=COMPANY_STATUS, default=10)


    class Meta:
        verbose_name = '公司表'
        verbose_name_plural = verbose_name
        ordering = ('-weight',)

    def __str__(self):
        return self.name
