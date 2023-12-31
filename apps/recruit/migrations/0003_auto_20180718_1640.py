# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-18 16:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recruit', '0002_auto_20180709_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='browse',
            name='recruit',
        ),
        migrations.RemoveField(
            model_name='browse',
            name='user',
        ),
        migrations.RemoveField(
            model_name='card',
            name='address',
        ),
        migrations.RemoveField(
            model_name='card',
            name='recruit',
        ),
        migrations.AlterUniqueTogether(
            name='cardsign',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='cardsign',
            name='card',
        ),
        migrations.RemoveField(
            model_name='cardsign',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='cardsignlog',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='cardsignlog',
            name='sign',
        ),
        migrations.RemoveField(
            model_name='cardsignlog',
            name='user',
        ),
        migrations.RemoveField(
            model_name='recruitorder',
            name='company',
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.ForeignKey(help_text='增加者', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='增加者'),
        ),
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.ForeignKey(help_text='公司地址', null=True, on_delete=django.db.models.deletion.CASCADE, to='area.Address', verbose_name='公司地址'),
        ),
        migrations.AlterField(
            model_name='company',
            name='weight',
            field=models.IntegerField(default=1, help_text='权重', verbose_name='权重'),
        ),
        migrations.DeleteModel(
            name='Browse',
        ),
        migrations.DeleteModel(
            name='Card',
        ),
        migrations.DeleteModel(
            name='CardSign',
        ),
        migrations.DeleteModel(
            name='CardSignLog',
        ),
        migrations.DeleteModel(
            name='RecruitOrder',
        ),
    ]
