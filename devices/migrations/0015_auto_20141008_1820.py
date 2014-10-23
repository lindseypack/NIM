# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0014_auto_20140930_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ups',
            name='brand',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Brand', blank=True),
        ),
        migrations.AlterField(
            model_name='ups',
            name='mac',
            field=models.CharField(default=b'', max_length=12, verbose_name=b'MAC', blank=True),
        ),
        migrations.AlterField(
            model_name='ups',
            name='mfdate',
            field=models.CharField(default=b'', max_length=10, verbose_name=b'Manufacture Date', blank=True),
        ),
        migrations.AlterField(
            model_name='ups',
            name='model',
            field=models.CharField(default=b'', max_length=32, verbose_name=b'Model', blank=True),
        ),
        migrations.AlterField(
            model_name='ups',
            name='name',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Name', blank=True),
        ),
        migrations.AlterField(
            model_name='ups',
            name='serialno',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Serial No', blank=True),
        ),
    ]
