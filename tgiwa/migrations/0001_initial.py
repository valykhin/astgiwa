# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-15 02:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Browser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('company', models.CharField(max_length=64)),
                ('version', models.CharField(max_length=64)),
                ('support_type', models.CharField(max_length=16)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('full_url', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='DefectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=512)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('scheduled_time', models.DateTimeField(blank=True, null=True)),
                ('priority', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Resolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
                ('aspect_ratio', models.CharField(max_length=8)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('file_path', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=1)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('finish_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('browser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgiwa.Browser')),
                ('resolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgiwa.Resolution')),
            ],
        ),
        migrations.CreateModel(
            name='TestRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=128)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=128)),
                ('port', models.IntegerField(blank=True, null=True)),
                ('endpoint', models.CharField(blank=True, max_length=512, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='testconfiguration',
            name='test_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgiwa.TestRequest'),
        ),
        migrations.AddField(
            model_name='test',
            name='test_configuration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgiwa.TestConfiguration'),
        ),
        migrations.AddField(
            model_name='test',
            name='url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgiwa.URL'),
        ),
        migrations.AddField(
            model_name='queue',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgiwa.Test'),
        ),
        migrations.AddField(
            model_name='defect',
            name='defect_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgiwa.DefectType'),
        ),
        migrations.AddField(
            model_name='defect',
            name='screenshot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgiwa.Screenshot'),
        ),
        migrations.AddField(
            model_name='defect',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tgiwa.Test'),
        ),
    ]
