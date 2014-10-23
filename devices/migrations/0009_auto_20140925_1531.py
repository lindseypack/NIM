# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0008_auto_20140919_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ap',
            name='laststatus',
            field=models.CharField(default=b'up', max_length=32, verbose_name=b'Last Status'),
        ),
    ]
