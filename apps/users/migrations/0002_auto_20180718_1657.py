# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-18 16:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0003_auto_20180709_1122'),
        ('recruit', '0003_auto_20180718_1640'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileextendinfo',
            name='admin_company',
            field=models.ForeignKey(help_text='企业用户', null=True, on_delete=django.db.models.deletion.CASCADE, to='recruit.Company', verbose_name='企业用户'),
        ),
        migrations.AddField(
            model_name='profileextendinfo',
            name='admin_school',
            field=models.ForeignKey(help_text='管理学校/区域(外键)', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_school', to='area.School', verbose_name='管理学校/区域'),
        ),
        migrations.AlterField(
            model_name='profileextendinfo',
            name='in_school',
            field=models.ForeignKey(blank=True, help_text='所在学校/区域(外键)', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='in_school', to='area.School', verbose_name='所在学校/区域'),
        ),
    ]
