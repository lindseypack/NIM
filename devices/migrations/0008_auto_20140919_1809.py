# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0007_auto_20140919_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ap',
            name='checkstatus',
            field=models.BooleanField(default=True, verbose_name=b'Check Status?'),
        ),
    ]
