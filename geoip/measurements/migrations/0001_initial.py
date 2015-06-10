# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0001_initial'),
        ('databases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='start time', blank=True)),
                ('end', models.DateTimeField(verbose_name='end time', blank=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('is_public', models.BooleanField(default=False, verbose_name='is public')),
            ],
            options={
                'get_latest_by': 'start',
                'verbose_name_plural': 'measurements',
                'verbose_name': 'measurement',
                'ordering': ['start'],
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('ipv4_location', django.contrib.gis.db.models.fields.PointField(geography=True, verbose_name='IPv4 location', srid=4326)),
                ('ipv6_location', django.contrib.gis.db.models.fields.PointField(geography=True, verbose_name='IPv6 location', srid=4326)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('database', models.ForeignKey(related_name='measurements', verbose_name='GeoIP database', on_delete=django.db.models.deletion.PROTECT, to='databases.Database')),
                ('dataset', models.ForeignKey(related_name='measurements', verbose_name='data set', to='measurements.Dataset')),
                ('node', models.ForeignKey(related_name='measurements', verbose_name='node', on_delete=django.db.models.deletion.PROTECT, to='nodes.Node')),
            ],
            options={
                'verbose_name_plural': 'measurements',
                'verbose_name': 'measurement',
                'ordering': ['dataset', 'database', 'created'],
            },
        ),
    ]
