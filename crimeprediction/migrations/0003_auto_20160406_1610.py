# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-06 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crimeprediction', '0002_auto_20160406_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crimesample',
            name='grids',
            field=models.ManyToManyField(related_name='samples', to='map.Grid'),
        ),
    ]
