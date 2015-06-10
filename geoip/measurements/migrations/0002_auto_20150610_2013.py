# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataset',
            options={'verbose_name': 'data set', 'ordering': ['start'], 'get_latest_by': 'start', 'verbose_name_plural': 'data sets'},
        ),
    ]
