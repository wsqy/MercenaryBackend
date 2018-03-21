from django.db import models
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
        return self.username
