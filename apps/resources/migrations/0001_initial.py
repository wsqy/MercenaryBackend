# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-29 16:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='资源分类')),
                ('title_cn', models.CharField(blank=True, max_length=64, null=True, verbose_name='资源分类英文名')),
                ('type', models.CharField(choices=[('1', '页面'), ('2', '图片'), ('3', '视频'), ('4', '文字')], max_length=2, verbose_name='资源分类类型')),
                ('weight', models.IntegerField(default=1, verbose_name='权重')),
                ('height', models.IntegerField(default=0, verbose_name='尺寸-高度')),
                ('width', models.IntegerField(default=0, verbose_name='尺寸-宽度')),
                ('image', models.ImageField(null=True, upload_to='resource/category', verbose_name='主页图标')),
                ('remark', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('is_active', models.BooleanField(default=True, help_text='是否激活', verbose_name='是否激活')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
        ),
        migrations.CreateModel(
            name='ResourceMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='资源名称')),
                ('subtitle', models.CharField(max_length=64, verbose_name='资源小标题')),
                ('title_cn', models.CharField(blank=True, max_length=64, null=True, verbose_name='资源名称英文名')),
                ('material', models.FileField(blank=True, null=True, upload_to='resource/material/%Y/%m', verbose_name='资源地址')),
                ('clink_url', models.URLField(blank=True, null=True, verbose_name='点击跳转地址')),
                ('weight', models.IntegerField(default=1, verbose_name='权重')),
                ('ext_value', models.CharField(blank=True, max_length=256, null=True, verbose_name='扩展字段')),
                ('inure_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='开始时间')),
                ('expire_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='过期时间')),
                ('remark', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('is_active', models.BooleanField(default=True, help_text='是否激活', verbose_name='是否激活')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.ResourceCategory', verbose_name='所属分类')),
            ],
        ),
    ]