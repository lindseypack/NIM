# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0017_remove_switch_autoupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='ap',
            name='model',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Model'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ups',
            name='brand',
            field=models.CharField(default=b'', max_length=50, verbose_name=b'Brand', blank=True, choices=[(b'Liebert', b'Liebert'), (b'APC', b'APC'), (b'LiebertNX', b'Liebert NX')]),
        ),
    ]
