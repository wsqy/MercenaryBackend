# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-28 15:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180709_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankcard',
            name='card_no',
            field=models.CharField(help_text='银行卡号', max_length=64, unique=True, verbose_name='银行卡号'),
        ),
        migrations.AlterField(
            model_name='bankcard',
            name='id_card',
            field=models.CharField(help_text='身份证', max_length=64, verbose_name='身份证'),
        ),
    ]
