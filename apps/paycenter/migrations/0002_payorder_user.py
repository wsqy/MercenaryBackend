# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-04 13:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('paycenter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payorder',
            name='user',
            field=models.ForeignKey(help_text='支付用户', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='支付用户'),
        ),
    ]
