# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0012_auto_20140925_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ap',
            name='notes',
            field=models.TextField(default=b'', verbose_name=b'Notes', blank=True),
        ),
        migrations.AlterField(
            model_name='phone',
            name='notes',
            field=models.TextField(default=b'', verbose_name=b'Notes', blank=True),
        ),
        migrations.AlterField(
            model_name='switch',
            name='notes',
            field=models.TextField(default=b'', verbose_name=b'Notes', blank=True),
        ),
        migrations.AlterField(
            model_name='ups',
            name='notes',
            field=models.TextField(default=b'', verbose_name=b'Notes', blank=True),
        ),
    ]
