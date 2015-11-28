# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20151128_1257'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalTransfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('description', models.CharField(default=None, max_length=500, null=True, blank=True)),
                ('prototype', models.ForeignKey(to='app.Prototype')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
