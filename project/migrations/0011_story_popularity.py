# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-09 01:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20170507_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='popularity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]