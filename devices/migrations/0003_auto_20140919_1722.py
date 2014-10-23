# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='AP',
            fields=[
                ('serialno', models.CharField(max_length=50, serialize=False, verbose_name=b'Serial No', primary_key=True)),
                ('ip', models.GenericIPAddressField(verbose_name=b'IP')),
                ('mac', models.CharField(default=b'', max_length=12, verbose_name=b'MAC')),
                ('name', models.CharField(default=b'', max_length=50, verbose_name=b'Name')),
                ('checkstatus', models.IntegerField(default=1, verbose_name=b'Check Status?')),
                ('laststatus', models.CharField(default=b'up', max_length=32, verbose_name=b'laststatus')),
                ('notes', models.TextField(default=b'', verbose_name=b'Notes')),
                ('autoupdate', models.IntegerField(default=1, verbose_name=b'Autoupdate?')),
                ('lastupdate', models.DateTimeField(auto_now=True, verbose_name=b'Last Update')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='switch',
            name='autoupdate',
            field=models.IntegerField(default=1, verbose_name=b'Autoupdate?'),
        ),
    ]
