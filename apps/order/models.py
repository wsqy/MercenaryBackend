from django.db import models
from utils.validators import IntRangeValidator


class Classification(models.Model):
    """
    订单一级分类
    """
    name = models.CharField(max_length=255, null=False, verbose_name='分类名', help_text='一级分类')
    weight = models.IntegerField(default=1, verbose_name='权重', help_text='权重',
                                 validators=IntRangeValidator())
    is_active = models.BooleanField(default=True, verbose_name='是否激活', help_text='是否激活')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '一级分类'
        verbose_name_plural = verbose_name
        ordering = ['weight']


class SubCategory(models.Model):
    """
    订单二级分类
    """
    name = models.CharField(max_length=255, null=False, verbose_name='分类名', help_text='二级分类')
    weight = models.IntegerField(default=1, verbose_name='权重', help_text='权重',
                                 validators=IntRangeValidator())
    is_active = models.BooleanField(default=True, verbose_name='是否激活', help_text='是否激活')
    classification = models.ForeignKey(Classification, verbose_name='父分类', help_text='所属分类')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '二级分类'
        verbose_name_plural = verbose_name
        ordering = ['weight']