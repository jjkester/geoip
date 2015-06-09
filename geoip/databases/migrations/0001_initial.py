# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('codename', models.CharField(max_length=255, unique=True, verbose_name='code name')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('version', models.CharField(max_length=255, verbose_name='version')),
                ('url', models.URLField(blank=True, verbose_name='website')),
                ('notes', models.TextField(blank=True, verbose_name='notes')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
            ],
            options={
                'ordering': ['-is_active', 'name'],
                'verbose_name': 'GeoIP database',
                'verbose_name_plural': 'GeoIP databases',
            },
        ),
    ]
