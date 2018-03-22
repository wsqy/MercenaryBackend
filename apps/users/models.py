from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class ProfileInfo(AbstractUser):
    """
    用户
    """
    nickname = models.CharField(max_length=30, null=True, blank=True,
                                verbose_name="用户昵称",
                                help_text='用户昵称 默认 用户+手机号后4位',)

    gender = models.NullBooleanField(null=True, blank=True, verbose_name='性别',
                                     help_text='未知时设置为 null')
    mobile = models.CharField(null=True, blank=True, max_length=15,
                              verbose_name='电话', help_text='用户手机号')
    portrait = models.CharField(null=True, blank=True, max_length=254,
                                verbose_name='头像',
                                help_text='用户头像地址 现阶段是阿里云OSS地址')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mobile


class AppInfo(models.Model):
    """
    设备
    """
    GENDER_CHOICES = (
        ('1', 'ios'),
        ('2', 'android'),
        ('3', '微信公众号'),
        ('4', '微信小程序'),
        ('5', '支付宝小程序'),
        ('6', '快应用'),
    )
    deviceid = models.CharField(max_length=40, blank=False, verbose_name='设备ID',
                                help_text='设备的唯一标识 mac地址 超过40位只保存40位')
    model = models.CharField(max_length=20, blank=True, verbose_name='设备型号',
                             help_text='类似于R9sPlus iPhone 6 等 超过20位只保存20位')
    device_ver = models.CharField(max_length=10, blank=True, verbose_name='设备版本号',
                                  help_text='设备的版本号 类似于 10.3.3 超过10位只保存10位')
    channel_code = models.CharField(max_length=2, blank=False, verbose_name='注册渠道号',
                                    help_text='注册渠道 目前只支持 ios 和android')
    date_joined = models.DateTimeField(verbose_name='注册时间', default=timezone.now)

    class Meta:
        verbose_name = "设备"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.deviceid
