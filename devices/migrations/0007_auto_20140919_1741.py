# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0006_ups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ups',
            name='id',
        ),
        migrations.AlterField(
            model_name='ups',
            name='ip',
            field=models.GenericIPAddressField(serialize=False, verbose_name=b'IP', primary_key=True),
        ),
    ]
