from django.db import models
from django.utils import timezone


class ResourceCategory(models.Model):
    """
    资源分类
    """
    RESOURCE_TYPE = (
        ('1', '页面'),
        ('2', '图片'),
        ('3', '视频'),
        ('4', '文字'),
    )
    title = models.CharField(max_length=32, null=False, verbose_name='资源分类')
    title_cn = models.CharField(max_length=64, null=True, blank=True, verbose_name='资源分类英文名')
    type = models.CharField(max_length=2, verbose_name='资源分类类型', choices=RESOURCE_TYPE)
    weight = models.IntegerField(default=1, verbose_name='权重')
    height = models.IntegerField(default=0, verbose_name='尺寸-高度')
    width = models.IntegerField(default=0, verbose_name='尺寸-宽度')
    image = models.ImageField(null=True, upload_to='resource/category', verbose_name='主页图标')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_active = models.BooleanField(default=True, verbose_name='是否激活', help_text='是否激活')
    modify_time = models.DateTimeField(auto_now=timezone.now, verbose_name='修改时间')

    class Meta:
        verbose_name = '资源分类'
        verbose_name_plural = verbose_name
        ordering = ('-modify_time',)

    def __str__(self):
        return self.title


class ResourceMaterial(models.Model):
    """
    资源文件
    """
    title = models.CharField(max_length=32, null=False, verbose_name='资源名称')
    subtitle = models.CharField(max_length=64, null=True, blank=True, verbose_name='资源小标题')
    title_cn = models.CharField(max_length=64, null=True, blank=True, verbose_name='资源名称英文名')
    category = models.ForeignKey(ResourceCategory, verbose_name='所属分类')
    material = models.FileField(upload_to='resource/material/%Y/%m', null=True, blank=True, verbose_name='资源地址')
    clink_url = models.URLField(null=True, blank=True, verbose_name='点击跳转地址')
    weight = models.IntegerField(default=1, verbose_name='权重')
    ext_value = models.CharField(max_length=256, null=True, blank=True, verbose_name='扩展字段')
    inure_time = models.DateTimeField(default=timezone.now, verbose_name='开始时间')
    expire_time = models.DateTimeField(default=timezone.now, verbose_name='过期时间')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_active = models.BooleanField(default=True, verbose_name='是否激活', help_text='是否激活')
    modify_time = models.DateTimeField(auto_now=timezone.now, verbose_name='修改时间')

    class Meta:
        verbose_name = '资源文件'
        verbose_name_plural = verbose_name
        ordering = ('-weight', '-modify_time',)

    def __str__(self):
        return self.title
