# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-17 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgiwa', '0006_url_test_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='protocol',
            field=models.CharField(default='http', max_length=8),
            preserve_default=False,
        ),
    ]
