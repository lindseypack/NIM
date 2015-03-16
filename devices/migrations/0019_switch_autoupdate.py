# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0018_auto_20150311_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='autoupdate',
            field=models.BooleanField(default=True, verbose_name=b'Autoupdate?'),
            preserve_default=True,
        ),
    ]
