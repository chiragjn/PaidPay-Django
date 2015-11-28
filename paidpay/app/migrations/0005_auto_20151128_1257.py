# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151128_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainuser',
            name='merchant_auth',
            field=models.CharField(default='akjsdghi8346r8yihudfjskdyie7oudisjlx', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mainuser',
            name='billing_address',
            field=models.CharField(default=None, max_length=400, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mainuser',
            name='shipping_address',
            field=models.CharField(default=None, max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
    ]
