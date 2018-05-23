# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-22 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20180411_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileextendinfo',
            name='balance',
            field=models.IntegerField(default=0, help_text='可用余额(分)', verbose_name='余额'),
        ),
        migrations.AddField(
            model_name='profileextendinfo',
            name='deposit_freeze',
            field=models.IntegerField(default=0, help_text='冻结金额(分)', verbose_name='冻结金额'),
        ),
        migrations.AddField(
            model_name='profileextendinfo',
            name='password',
            field=models.CharField(blank=True, help_text='支付密码(暂时不用)', max_length=128, null=True, verbose_name='支付密码'),
        ),
        migrations.AddField(
            model_name='profileextendinfo',
            name='remark',
            field=models.TextField(blank=True, help_text='备注信息', null=True, verbose_name='备注信息'),
        ),
        migrations.AlterField(
            model_name='profileextendinfo',
            name='jpush_token',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='极光推送Token'),
        ),
        migrations.AlterField(
            model_name='profileextendinfo',
            name='origin_mobile',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='推荐人手机号'),
        ),
        migrations.AlterField(
            model_name='profileextendinfo',
            name='rongcloud_token',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='融云IM Token'),
        ),
    ]