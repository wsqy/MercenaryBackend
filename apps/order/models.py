from django.db import models
from utils.validators import IntRangeValidator


class SubCategory(models.Model):
    """
    订单二级分类
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
    name = models.CharField(max_length=255, null=False, verbose_name='分类名', help_text='二级分类')
    weight = models.IntegerField(default=1, verbose_name='权重', help_text='权重',
                                 validators=IntRangeValidator())
    is_active = models.BooleanField(default=True, verbose_name='是否激活', help_text='是否激活')
    classification = models.IntegerField(choices=CLASSIFICATION_CHOICE, default=1,
                                         verbose_name='父分类', help_text='所属分类')
    template = models.IntegerField(choices=TEMPLATE_CHOICE, default=1,
                                   verbose_name='分类模板', help_text='分类数据所使用的模板')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['-weight']

