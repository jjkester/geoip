# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('url', models.URLField(verbose_name='URL')),
            ],
            options={
                'verbose_name_plural': 'sources',
                'verbose_name': 'source',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('dns_name', models.CharField(max_length=255, verbose_name='domain name', blank=True)),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326, verbose_name='known location', null=True, blank=True)),
                ('ipv4', models.GenericIPAddressField(verbose_name='IPv4 address', null=True, blank=True, protocol='ipv4')),
                ('ipv6', models.GenericIPAddressField(verbose_name='IPv6 address', null=True, blank=True, protocol='ipv6')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('is_active', models.BooleanField(verbose_name='is active', default=True)),
                ('source', models.ForeignKey(to='nodes.DataSource', verbose_name='source', related_name='nodes+', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name_plural': 'nodes',
                'verbose_name': 'node',
            },
        ),
    ]
