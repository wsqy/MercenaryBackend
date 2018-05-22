# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-22 17:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_type', models.CharField(choices=[('10', '跑腿单佣金'), ('20', '招募令佣金'), ('30', '提现')], help_text='变动类型', max_length=5, verbose_name='变动类型')),
                ('balance', models.IntegerField(default=0, help_text='变动金额(分)', verbose_name='金额')),
                ('remark', models.CharField(blank=True, help_text='备注信息', max_length=128, null=True, verbose_name='备注信息')),
                ('user', models.ForeignKey(help_text='用户', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '账户余额变动表',
                'verbose_name_plural': '账户余额变动表',
            },
        ),
    ]
