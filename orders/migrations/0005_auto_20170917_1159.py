# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-17 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20170917_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='type',
            field=models.CharField(choices=[('image', 'Image'), ('text', 'Text')], max_length=16),
        ),
    ]