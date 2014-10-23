# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_auto_20140919_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='ap',
            name='test',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
