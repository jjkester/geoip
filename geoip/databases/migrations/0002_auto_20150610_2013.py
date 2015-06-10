# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import re


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database',
            name='codename',
            field=models.CharField(max_length=255, verbose_name='code name', validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+$', 32), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')], unique=True),
        ),
    ]
