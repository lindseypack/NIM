# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_ap_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ap',
            name='test',
        ),
        migrations.AlterField(
            model_name='ap',
            name='autoupdate',
            field=models.BooleanField(default=True, verbose_name=b'Autoupdate?'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='autoupdate',
            field=models.BooleanField(default=True, verbose_name=b'Autoupdate?'),
        ),
    ]
