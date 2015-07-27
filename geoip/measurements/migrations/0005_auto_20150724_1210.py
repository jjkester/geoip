# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0004_auto_20150724_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='ipv4_location',
            field=django.contrib.gis.db.models.fields.PointField(verbose_name='IPv4 location', null=True, geography=True, srid=4326, blank=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='ipv6_location',
            field=django.contrib.gis.db.models.fields.PointField(verbose_name='IPv6 location', null=True, geography=True, srid=4326, blank=True),
        ),
    ]
