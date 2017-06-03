# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='userInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=20)),
                ('passwd', models.CharField(max_length=40)),
                ('umail', models.CharField(max_length=40)),
                ('utel', models.CharField(default=b'', max_length=15)),
                ('upost', models.CharField(default=b'', max_length=11)),
                ('uaddress', models.CharField(default=b'', max_length=40)),
                ('ushou', models.CharField(default=b'', max_length=40)),
            ],
        ),
    ]
