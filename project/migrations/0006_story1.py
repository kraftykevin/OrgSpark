# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 04:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20170403_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('para', models.TextField()),
            ],
        ),
    ]
