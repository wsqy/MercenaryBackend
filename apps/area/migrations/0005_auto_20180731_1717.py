# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-31 17:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0004_auto_20180731_1710'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='school',
            options={'ordering': ('pinyin', '-weight'), 'verbose_name': '学校/区域', 'verbose_name_plural': '学校/区域'},
        ),
    ]
