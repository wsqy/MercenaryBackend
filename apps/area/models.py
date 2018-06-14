from django.db import models

import pygeohash

from utils.common import to_number

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

    @staticmethod
    def clear_name(name):
        """
        对省份名称进行格式化
        :param name: 省份名称
        :return: 格式化后的省份名称
        """
        suffix_list = ['回族自治区', '壮族自治区', '维吾尔自治区', '特别行政区', '直辖市', '自治区', '省', '市']
        for suffix in suffix_list:
            name = name.rstrip(suffix)
        return name


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
        return '{}-{}'.format(self.province, self.name)

    @staticmethod
    def clear_name(name):
        """
        对市名称进行格式化
        :param name: 市名称
        :return: 格式化后的市名称
        """
        suffix_list = ['特别行政区', '直辖市', '市']
        for suffix in suffix_list:
            name = name.rstrip(suffix)
        return name


class District(models.Model):
    """
    城市
    """
    name = models.CharField(blank=False, max_length=32, verbose_name='城市')
    city = models.ForeignKey(City, verbose_name="市")

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}-{}'.format(self.city, self.name)

    @staticmethod
    def clear_name(name):
        """
        对城市名称进行格式化
        :param name: 城市名称
        :return: 格式化后的城市名称
        """
        suffix_list = ['县', '区']
        for suffix in suffix_list:
            name = name.rstrip(suffix)
        return name



class School(models.Model):
    """
    学校表
    经纬度请使用百度地图查询
    """
    name = models.CharField(blank=False, null=False, max_length=32, verbose_name='学校', help_text='学校')
    city = models.ForeignKey(City, verbose_name='市', help_text='所属市')
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
