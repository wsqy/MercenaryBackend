# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-26 16:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0009_auto_20180525_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithDraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('1', '银行卡')], default='1', help_text='提现去向', max_length=2, verbose_name='提现去向')),
                ('account', models.CharField(blank=True, help_text='提现账号', max_length=64, null=True, verbose_name='提现账号')),
                ('balance', models.IntegerField(default=0, help_text='提现金额(分)', verbose_name='金额')),
                ('status', models.CharField(choices=[('1', '银行卡')], default='1', help_text='提现状态', max_length=1, verbose_name='状态')),
                ('remark', models.CharField(blank=True, help_text='备注信息', max_length=128, null=True, verbose_name='备注信息')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, help_text='申请时间', verbose_name='申请时间')),
                ('user', models.ForeignKey(help_text='用户', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '提现信息表',
                'verbose_name_plural': '提现信息表',
                'ordering': ('-add_time',),
            },
        ),
    ]