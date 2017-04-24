# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacherapp', '0001_initial'),
        ('commonapp', '0006_auto_20170423_1930'),
    ]

    operations = [
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('courseid', models.ForeignKey(to='teacherapp.Course_t')),
            ],
        ),
    ]
