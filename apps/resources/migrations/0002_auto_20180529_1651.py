# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-29 16:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resourcecategory',
            options={'ordering': ('-modify_time',), 'verbose_name': '资源分类', 'verbose_name_plural': '资源分类'},
        ),
        migrations.AlterModelOptions(
            name='resourcematerial',
            options={'ordering': ('-modify_time',), 'verbose_name': '资源文件', 'verbose_name_plural': '资源文件'},
        ),
    ]
