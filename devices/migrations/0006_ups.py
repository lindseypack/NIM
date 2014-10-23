# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_auto_20140919_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='UPS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField(verbose_name=b'IP')),
                ('name', models.CharField(default=b'', max_length=50, verbose_name=b'Name')),
                ('mac', models.CharField(default=b'', max_length=12, verbose_name=b'MAC')),
                ('model', models.CharField(default=b'', max_length=32, verbose_name=b'Model')),
                ('serialno', models.CharField(default=b'', max_length=50, verbose_name=b'Serial No')),
                ('mfdate', models.CharField(default=b'', max_length=10, verbose_name=b'Manufacture Date')),
                ('brand', models.CharField(default=b'', max_length=50, verbose_name=b'Brand')),
                ('notes', models.TextField(default=b'', verbose_name=b'Notes')),
                ('autoupdate', models.BooleanField(default=True, verbose_name=b'Autoupdate?')),
                ('lastupdate', models.DateTimeField(auto_now=True, verbose_name=b'Last Update')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
