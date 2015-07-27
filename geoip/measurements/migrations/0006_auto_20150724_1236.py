# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0005_auto_20150724_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='ipv4_distance',
            field=models.FloatField(verbose_name='IPv4 distance', null=True, blank=True, editable=False),
        ),
        migrations.AddField(
            model_name='measurement',
            name='ipv6_distance',
            field=models.FloatField(verbose_name='IPv6 distance', null=True, blank=True, editable=False),
        ),
        migrations.AddField(
            model_name='measurement',
            name='mutual_distance',
            field=models.FloatField(verbose_name='mutual distance', null=True, blank=True, editable=False),
        ),
    ]
