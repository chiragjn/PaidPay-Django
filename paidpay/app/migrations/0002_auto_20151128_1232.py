# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainuser',
            name='email_address',
            field=models.CharField(default='john@cena.com', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mainuser',
            name='phone_number',
            field=models.CharField(default='9930112199', max_length=400),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mainuser',
            name='address',
            field=models.CharField(default=None, max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
    ]
