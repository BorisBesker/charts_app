# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 18:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_charts', '0003_savelocation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationsave',
            name='user',
        ),
        migrations.DeleteModel(
            name='LocationSave',
        ),
    ]
