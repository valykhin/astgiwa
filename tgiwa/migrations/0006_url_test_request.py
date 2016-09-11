# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-15 08:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgiwa', '0005_browser_operating_system'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='test_request',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tgiwa.TestRequest'),
            preserve_default=False,
        ),
    ]
