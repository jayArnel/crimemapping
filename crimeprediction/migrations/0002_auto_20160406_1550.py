# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-06 15:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crimeprediction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crimesample',
            old_name='grid',
            new_name='grids',
        ),
    ]
