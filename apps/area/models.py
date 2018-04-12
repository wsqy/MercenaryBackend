from django.db import models


class Province(models.Model):
    """
    省份表
    """
    name = models.CharField(blank=False, max_length=20, verbose_name='省份')

    class Meta:
        verbose_name = '省份'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class City(models.Model):
    """
    市表
    """
    name = models.CharField(blank=False, max_length=32, verbose_name='市')
    province = models.ForeignKey(Province, verbose_name="省")

    class Meta:
        verbose_name = '市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Country(models.Model):
    """
    城市
    """
    name = models.CharField(blank=False, max_length=32, verbose_name='城市')
    city = models.ForeignKey(City, verbose_name="市")

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

