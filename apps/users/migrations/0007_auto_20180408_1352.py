# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-08 13:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180323_1013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='verifycode',
            options={'ordering': ['-expire_time'], 'verbose_name': '短信验证码', 'verbose_name_plural': '短信验证码'},
        ),
        migrations.AlterField(
            model_name='profileinfo',
            name='mobile',
            field=models.CharField(blank=True, help_text='手机号码', max_length=15, verbose_name='手机号码'),
        ),
        migrations.AlterField(
            model_name='verifycode',
            name='code',
            field=models.CharField(help_text='验证码', max_length=10, verbose_name='验证码'),
        ),
        migrations.AlterField(
            model_name='verifycode',
            name='expire_time',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='过期时间', verbose_name='过期时间'),
        ),
        migrations.AlterField(
            model_name='verifycode',
            name='mobile',
            field=models.CharField(help_text='手机号', max_length=11, verbose_name='手机号'),
        ),
        migrations.AlterField(
            model_name='verifycode',
            name='type',
            field=models.CharField(choices=[('SMS_76310006', '注册验证码'), ('SMS_76270012', '找回密码验证码')], help_text='验证码类型', max_length=12, verbose_name='验证码类别'),
        ),
    ]