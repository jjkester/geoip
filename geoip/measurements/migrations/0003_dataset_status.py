# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0002_auto_20150610_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='status',
            field=models.SmallIntegerField(verbose_name='status', default=(0, 'queued'), choices=[('queued', (0, 'queued')), ('running', (1, 'running')), ('success', (2, 'success')), ('error', (-1, 'error'))]),
        ),
    ]
