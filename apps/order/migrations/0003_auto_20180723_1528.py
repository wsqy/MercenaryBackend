# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-23 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20180709_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderinfo',
            name='from_addr_district',
        ),
        migrations.RemoveField(
            model_name='orderinfo',
            name='to_addr_district',
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='category',
            field=models.PositiveSmallIntegerField(choices=[(1, '即时'), (2, '顺风'), (3, '替身'), (4, '技能'), (5, '活动')], default=1, help_text='所属父分类', verbose_name='所属父分类'),
        ),
    ]
