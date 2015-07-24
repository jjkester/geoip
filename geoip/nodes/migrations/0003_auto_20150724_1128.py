# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0002_auto_20150610_2013'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='node',
            options={'verbose_name': 'node', 'verbose_name_plural': 'nodes', 'ordering': ['created']},
        ),
    ]
