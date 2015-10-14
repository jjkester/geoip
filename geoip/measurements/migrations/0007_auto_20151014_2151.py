# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0006_auto_20150724_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='ipv4_distance',
            field=models.FloatField(null=True, blank=True, verbose_name='IPv4 distance'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='ipv6_distance',
            field=models.FloatField(null=True, blank=True, verbose_name='IPv6 distance'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='mutual_distance',
            field=models.FloatField(null=True, blank=True, verbose_name='mutual distance'),
        ),
    ]
