# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0009_auto_20140925_1531'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ap',
            options={'verbose_name': 'Access Point'},
        ),
    ]
