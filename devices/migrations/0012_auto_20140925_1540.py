# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0011_auto_20140925_1536'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ap',
            options={'ordering': ['name'], 'verbose_name': 'Access Point'},
        ),
    ]
