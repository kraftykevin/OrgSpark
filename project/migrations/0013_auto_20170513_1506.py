# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-13 22:06
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_auto_20170510_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='finished_story',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='story',
            name='vote_minimum',
            field=models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='story',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='title'),
        ),
    ]
