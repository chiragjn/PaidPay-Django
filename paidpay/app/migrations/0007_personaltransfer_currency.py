# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_personaltransfer'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaltransfer',
            name='currency',
            field=models.IntegerField(default=1, choices=[(1, b'INR'), (2, b'USD'), (3, b'GBP')]),
            preserve_default=False,
        ),
    ]
