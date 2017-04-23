# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacherapp', '0001_initial'),
        ('commonapp', '0003_auto_20170422_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stumess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stuname', models.CharField(max_length=100)),
                ('question', models.TextField()),
                ('courseid', models.ForeignKey(to='teacherapp.Course_t')),
            ],
        ),
    ]
