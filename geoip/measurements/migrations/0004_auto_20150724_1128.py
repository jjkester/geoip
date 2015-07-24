# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0003_dataset_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='measurement',
            options={'verbose_name': 'measurement', 'verbose_name_plural': 'measurements', 'ordering': ['dataset', 'database', 'created'], 'get_latest_by': 'created'},
        ),
        migrations.AlterField(
            model_name='dataset',
            name='end',
            field=models.DateTimeField(verbose_name='end time', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='start',
            field=models.DateTimeField(verbose_name='start time', blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='measurement',
            unique_together=set([('node', 'dataset', 'database')]),
        ),
    ]
