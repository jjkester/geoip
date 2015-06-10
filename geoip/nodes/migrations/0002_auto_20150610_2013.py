# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='source',
            field=models.ForeignKey(verbose_name='source', to='nodes.DataSource', related_name='nodes', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
