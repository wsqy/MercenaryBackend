# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-31 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0003_auto_20180709_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='first_pinyin',
            field=models.CharField(blank=True, help_text='首个名称首字母', max_length=32, null=True, verbose_name='首个名称首字母'),
        ),
        migrations.AddField(
            model_name='school',
            name='pinyin',
            field=models.CharField(blank=True, help_text='名称首字母', max_length=32, null=True, verbose_name='名称首字母'),
        ),
    ]
