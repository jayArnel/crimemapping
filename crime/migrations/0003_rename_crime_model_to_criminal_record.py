# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-06 15:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crime', '0002_crime_location'),
    ]

    operations = [
        migrations.RenameModel('Crime', 'CriminalRecord')
    ]
