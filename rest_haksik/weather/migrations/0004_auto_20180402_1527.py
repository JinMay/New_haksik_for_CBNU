# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-02 06:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_weather_cloud'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weather',
            old_name='cloud',
            new_name='humidity',
        ),
    ]