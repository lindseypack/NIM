# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Switch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serialno', models.CharField(default=b'', max_length=50, verbose_name=b'Serial No')),
                ('ip', models.GenericIPAddressField(verbose_name=b'IP')),
                ('name', models.CharField(default=b'', max_length=50, verbose_name=b'Name')),
                ('mac', models.CharField(default=b'', max_length=12, verbose_name=b'MAC')),
                ('model', models.CharField(default=b'', max_length=50, verbose_name=b'Model')),
                ('softwarever', models.CharField(default=b'', max_length=20, verbose_name=b'Software Version')),
                ('uptime', models.CharField(default=b'', max_length=50, verbose_name=b'Uptime')),
                ('stack', models.IntegerField(default=0, verbose_name=b'Stack')),
                ('purchaseyr', models.CharField(default=b'', max_length=4, verbose_name=b'Purchase Year')),
                ('purchaseorder', models.CharField(default=b'', max_length=50, verbose_name=b'Purchase Order')),
                ('uplink1', models.TextField(default=b'', verbose_name=b'Uplink 1')),
                ('uplink2', models.TextField(default=b'', verbose_name=b'Uplink 2')),
                ('uplink3', models.TextField(default=b'', verbose_name=b'Uplink 3')),
                ('uplink4', models.TextField(default=b'', verbose_name=b'Uplink 4')),
                ('notes', models.TextField(default=b'', verbose_name=b'Notes')),
                ('autoupdate', models.IntegerField(default=1, verbose_name=b'Autoupdate')),
                ('status', models.CharField(default=b'active', max_length=128, verbose_name=b'Status')),
                ('lastupdate', models.DateTimeField(auto_now=True, verbose_name=b'Last Update')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
