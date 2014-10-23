# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0013_auto_20140925_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='mac',
            field=models.CharField(default=b'', max_length=12, verbose_name=b'MAC', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='model',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Model', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='name',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Name', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='purchaseorder',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Purchase Order', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='purchaseyr',
            field=models.CharField(default=b'', max_length=4, verbose_name=b'Purchase Year', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='serialno',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Serial No', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='softwarever',
            field=models.CharField(default=b'', max_length=20, verbose_name=b'Software Version', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='stack',
            field=models.IntegerField(default=0, verbose_name=b'Stack', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='status',
            field=models.CharField(default=b'active', max_length=128, verbose_name=b'Status', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='uplink1',
            field=models.TextField(default=b'', verbose_name=b'Uplink 1', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='uplink2',
            field=models.TextField(default=b'', verbose_name=b'Uplink 2', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='uplink3',
            field=models.TextField(default=b'', verbose_name=b'Uplink 3', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='uplink4',
            field=models.TextField(default=b'', verbose_name=b'Uplink 4', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='uptime',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Uptime', blank=True),
        ),
    ]
