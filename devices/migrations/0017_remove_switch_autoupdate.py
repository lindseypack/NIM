# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0016_auto_20141014_1305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='switch',
            name='autoupdate',
        ),
    ]
