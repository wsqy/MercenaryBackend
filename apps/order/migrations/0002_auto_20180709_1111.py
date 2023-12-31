# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-09 11:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('area', '0002_address_user'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderoperatelog',
            name='user',
            field=models.ForeignKey(blank=True, help_text='操作用户', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='操作用户'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='category',
            field=models.ForeignKey(help_text='订单分类', on_delete=django.db.models.deletion.CASCADE, to='order.SubCategory', verbose_name='分类'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='create_district',
            field=models.ForeignKey(help_text='订单创建的城市', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_district', to='area.District', verbose_name='订单创建的城市'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='employer_user',
            field=models.ForeignKey(help_text='雇主', on_delete=django.db.models.deletion.CASCADE, related_name='employer_user', to=settings.AUTH_USER_MODEL, verbose_name='雇主'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='from_addr_district',
            field=models.ForeignKey(help_text='订单开始的城市', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_district', to='area.District', verbose_name='订单开始的城市'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='receiver_user',
            field=models.ForeignKey(help_text='佣兵', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver_user', to=settings.AUTH_USER_MODEL, verbose_name='佣兵'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='school',
            field=models.ForeignKey(blank=True, help_text='学院', null=True, on_delete=django.db.models.deletion.CASCADE, to='area.School', verbose_name='学校'),
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='to_addr_district',
            field=models.ForeignKey(help_text='订单结束的城市', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_district', to='area.District', verbose_name='订单结束的城市'),
        ),
    ]
