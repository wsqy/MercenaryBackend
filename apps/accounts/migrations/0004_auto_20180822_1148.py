# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-22 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180728_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankcard',
            name='card_no',
            field=models.CharField(help_text='银行卡号', max_length=64, verbose_name='银行卡号'),
        ),
        migrations.AlterField(
            model_name='withdraw',
            name='type',
            field=models.CharField(choices=[('1', '支付宝'), ('2', '微信'), ('4', '银行卡')], default='1', help_text='提现去向', max_length=2, verbose_name='提现去向'),
        ),
    ]