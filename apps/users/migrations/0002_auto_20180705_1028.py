# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-05 10:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileextendinfo',
            name='in_school',
            field=models.IntegerField(blank=True, help_text='所在学校/区域(外键)', null=True, verbose_name='所在学校/区域'),
        ),
    ]
