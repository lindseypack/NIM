# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0010_auto_20140925_1533'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phone',
            options={'verbose_name': 'Phone'},
        ),
        migrations.AlterModelOptions(
            name='switch',
            options={'verbose_name': 'Switch', 'verbose_name_plural': 'Switches'},
        ),
        migrations.AlterModelOptions(
            name='ups',
            options={'verbose_name': 'UPS', 'verbose_name_plural': 'UPSes'},
        ),
    ]
