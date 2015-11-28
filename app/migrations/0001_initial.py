# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MainUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('address', models.CharField(default=None, max_length=300, null=True, blank=True)),
                ('PAN', models.CharField(unique=True, max_length=400)),
                ('billing_address', models.CharField(default=None, max_length=400, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=400)),
                ('email_address', models.CharField(max_length=400)),
                ('shipping_address', models.CharField(default=None, max_length=500, null=True, blank=True)),
                ('PIN', models.CharField(max_length=4)),
                ('balance', models.DecimalField(max_digits=100, decimal_places=5)),
                ('payee_name', models.CharField(max_length=100)),
                ('type', models.IntegerField(default=1, choices=[(1, b'Merchant'), (2, b'Customer without PAN'), (3, b'Customer with PAN')])),
                ('gcm', models.CharField(max_length=500)),
                ('merchant_auth', models.CharField(max_length=200)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonalTransfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('description', models.CharField(default=None, max_length=500, null=True, blank=True)),
                ('currency', models.IntegerField(choices=[(1, b'INR'), (2, b'USD'), (3, b'GBP')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('sku', models.CharField(default=None, max_length=500, null=True, blank=True)),
                ('manufacturer', models.CharField(default=None, max_length=500, null=True, blank=True)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('quantity', models.IntegerField(default=1, blank=True)),
                ('currency', models.IntegerField(choices=[(1, b'INR'), (2, b'USD'), (3, b'GBP')])),
                ('description', models.CharField(default=None, max_length=500, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prototype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('merchant', models.ForeignKey(to='app.MainUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(choices=[(1, b'Successful and Remitted'), (2, b'Successful and Not Remitted'), (3, b'Failed')])),
                ('mode', models.IntegerField(choices=[(1, b'Citrus'), (2, b'PayU'), (3, b'PayPal'), (4, b'Barclays Card'), (5, b'Credit Card'), (6, b'Debit Card'), (7, b'PayTM'), (8, b'Google Wallet'), (9, b'Ola Wallet'), (10, b'MobiWik'), (11, b'Oxigen')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(to='app.MainUser')),
                ('prototype', models.ForeignKey(to='app.Prototype')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='prototype',
            field=models.ForeignKey(to='app.Prototype'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personaltransfer',
            name='prototype',
            field=models.ForeignKey(to='app.Prototype'),
            preserve_default=True,
        ),
    ]
