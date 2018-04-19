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
        return self.name

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
        return self.name

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

