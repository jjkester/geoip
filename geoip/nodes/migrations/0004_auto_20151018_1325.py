# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0003_auto_20150724_1128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='node',
            options={'get_latest_by': 'last_updated', 'verbose_name_plural': 'nodes', 'verbose_name': 'node', 'ordering': ['created']},
        ),
    ]
