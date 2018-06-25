import pygeohash
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from utils.common import to_number
from area.models import District


class DeviceInfo(models.Model):
    """
    设备
    """
    CHANNEL_CODE = (
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
    channel_code = models.CharField(max_length=2, blank=False, choices=CHANNEL_CODE,
                                    verbose_name='注册渠道号',
                                    help_text='注册渠道 目前只支持 ios 和android')
    date_joined = models.DateTimeField(verbose_name='注册时间', default=timezone.now)

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.deviceid


class School(models.Model):
    """
    学校表
    经纬度请使用百度地图查询
    """
    name = models.CharField(blank=False, null=False, max_length=32, verbose_name='学校', help_text='学校')
    district = models.ForeignKey(District, verbose_name='区', help_text='所属区')
    latitude = models.CharField(blank=False, null=False, max_length=32, verbose_name='纬度', help_text='纬度')
    longitude = models.CharField(blank=False, null=False, max_length=32, verbose_name='经度', help_text='经度')
    geohash = models.CharField(blank=True, null=True, max_length=12, verbose_name='geohash', help_text='geohash')
    is_active = models.BooleanField(default=True, verbose_name='是否激活', help_text='是否激活')
    weight = models.IntegerField(default=1, verbose_name='权重')

    class Meta:
        verbose_name = '学校'
        verbose_name_plural = verbose_name
        ordering = ('-weight', )

    def __str__(self):
        return self.name

    @staticmethod
    def get_geohash(lat, lon, deep=12, need='[null]'):
        """
        lat: 纬度
        lon: 经度
        deep: 深度 默认12
        need: 是否需要在错误时也返回一个值, 注意改数值最好不与geohash出现的字符重复
        """
        lat = to_number(lat)
        lon = to_number(lon)
        if lat and lon:
            return pygeohash.encode(lat, lon, deep)
        if need:
            return need

    def save(self, *args, **kwargs):
        """
        保存时自动重算geohash
        """
        self.geohash = self.get_geohash(self.latitude, self.longitude)
        super(School, self).save(*args, **kwargs)


class ProfileInfo(AbstractUser):
    """
    用户
    """
    nickname = models.CharField(max_length=30, blank=True, verbose_name='用户昵称',
                                help_text='用户昵称 默认 用户+手机号后4位',)
    gender = models.NullBooleanField(null=True, blank=True, verbose_name='性别',
                                     help_text='未知时设置为 null')
    mobile = models.CharField(blank=True, max_length=15, verbose_name='手机号码', help_text='手机号码')
    portrait = models.ImageField(blank=True, verbose_name='头像', upload_to='portrait/%Y/%m/%d',
                                 help_text='用户头像地址 现阶段是阿里云OSS地址')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname


class ProfileExtendInfo(models.Model):
    """
    用户扩展信息
    """
    user = models.ForeignKey(ProfileInfo, blank=True, null=True)
    device_join = models.ForeignKey(DeviceInfo, blank=True, null=True,
                                    verbose_name='用户注册时的设备')
    origin_mobile = models.CharField(blank=True, null=True, max_length=15,
                                     verbose_name='推荐人手机号')
    rongcloud_token = models.CharField(blank=True, null=True, max_length=100,
                                       verbose_name='融云IM Token')
    jpush_token = models.CharField(blank=True, null=True, max_length=100,
                                   verbose_name='极光推送Token')

    balance = models.IntegerField(default=0, verbose_name='余额', help_text='可用余额(分)')

    deposit_freeze = models.IntegerField(default=0, verbose_name='冻结金额', help_text='冻结金额(分)')

    password = models.CharField(verbose_name='支付密码', help_text='支付密码(暂时不用)',
                                max_length=128, blank=True, null=True, )

    remark = models.TextField(verbose_name='备注信息', blank=True, null=True, help_text='备注信息')
    in_school = models.ForeignKey(School, blank=True, null=True, related_name='in_school',
                                  verbose_name='属于学校', help_text='属于学校')
    admin_school = models.ForeignKey(School, verbose_name='管理的学校', related_name='admin_school',
                                     help_text='管理的学校', blank=True, null=True)

    class Meta:
        verbose_name = '用户扩展信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nickname


class VerifyCode(models.Model):
    """
    短信验证码
    """
    type = models.CharField(max_length=12, verbose_name='验证码类别',
                            choices=tuple(settings.CODE_TYPE.items()),
                            help_text='验证码类型')
    code = models.CharField(max_length=10, verbose_name='验证码', help_text='验证码')
    mobile = models.CharField(max_length=11, verbose_name='手机号', help_text='手机号')
    try_time = models.PositiveSmallIntegerField(default=3, verbose_name='剩余尝试次数',
                                                help_text='默认3,当验证成功时删除,0时删除',)
    expire_time = models.DateTimeField(default=timezone.now, verbose_name='过期时间',
                                       help_text='过期时间')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name
        ordering = ['-expire_time']



class Address(models.Model):
    """
    地址表
    经纬度请使用百度地图查询
    """
    name = models.CharField(blank=False, null=False, max_length=32, verbose_name='地点', help_text='地点')
    detail = models.CharField(blank=True, null=True, max_length=32, verbose_name='详细地点', help_text='详细地点')
    district = models.ForeignKey(District, verbose_name='区', help_text='所属区')
    latitude = models.CharField(blank=False, null=False, max_length=32, verbose_name='纬度', help_text='纬度')
    longitude = models.CharField(blank=False, null=False, max_length=32, verbose_name='经度', help_text='经度')
    geohash = models.CharField(blank=True, null=True, max_length=12, verbose_name='geohash', help_text='geohash')
    is_active = models.BooleanField(default=True, verbose_name='是否激活', help_text='是否激活')
    weight = models.IntegerField(default=1, verbose_name='权重', help_text='权重')
    user = models.ForeignKey(ProfileInfo, null=True, verbose_name='增加者', help_text='增加者')

    class Meta:
        verbose_name = '地址'
        verbose_name_plural = verbose_name
        ordering = ('-weight', )

    def __str__(self):
        return self.name

    @staticmethod
    def get_geohash(lat, lon, deep=12, need='[null]'):
        """
        lat: 纬度
        lon: 经度
        deep: 深度 默认12
        need: 是否需要在错误时也返回一个值, 注意改数值最好不与geohash出现的字符重复
        """
        lat = to_number(lat)
        lon = to_number(lon)
        if lat and lon:
            return pygeohash.encode(lat, lon, deep)
        if need:
            return need

    def save(self, *args, **kwargs):
        """
        保存时自动重算geohash
        """
        self.geohash = self.get_geohash(self.latitude, self.longitude)
        super(Address, self).save(*args, **kwargs)
