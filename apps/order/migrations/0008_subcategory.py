# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-06 10:26
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_delete_subcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='二级分类', max_length=255, verbose_name='分类名')),
                ('weight', models.IntegerField(default=1, help_text='权重', validators=[django.core.validators.MinValueValidator(1, message='不能小于%(limit_value)s.'), django.core.validators.MaxValueValidator(100, message='不能大于%(limit_value)s.')], verbose_name='权重')),
                ('is_active', models.BooleanField(default=True, help_text='是否激活', verbose_name='是否激活')),
                ('classification', models.PositiveSmallIntegerField(choices=[(1, '即时'), (2, '顺风'), (3, '替身'), (4, '技能'), (5, '活动')], default=1, help_text='所属分类', verbose_name='父分类')),
                ('template', models.PositiveSmallIntegerField(choices=[(1, '描述'), (2, '商品'), (3, '快递')], default=1, help_text='分类数据所使用的模板', verbose_name='分类模板')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'ordering': ['-weight'],
            },
        ),
    ]