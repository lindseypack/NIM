# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('name', models.CharField(max_length=32, serialize=False, verbose_name=b'Name', primary_key=True)),
                ('ip', models.GenericIPAddressField(verbose_name=b'IP')),
                ('mac', models.CharField(default=b'', max_length=12, verbose_name=b'MAC')),
                ('did', models.CharField(default=b'', max_length=10, verbose_name=b'DID')),
                ('model', models.CharField(default=b'', max_length=32, verbose_name=b'Model')),
                ('serialno', models.CharField(default=b'', max_length=50, verbose_name=b'Serial No')),
                ('status', models.CharField(default=b'', max_length=50, verbose_name=b'Status')),
                ('purchaseyr', models.CharField(default=b'', max_length=4, verbose_name=b'Purchase Year')),
                ('description', models.CharField(default=b'', max_length=200, verbose_name=b'Description')),
                ('notes', models.TextField(default=b'', verbose_name=b'Notes')),
                ('lastupdate', models.DateTimeField(auto_now=True, verbose_name=b'Last Update')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
