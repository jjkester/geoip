# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import re


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0002_auto_20150610_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='codename',
            field=models.CharField(verbose_name='code name', validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z', 32), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')], unique=True, max_length=255),
        ),
    ]
