# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacherapp', '0001_initial'),
        ('commonapp', '0004_stumess'),
    ]

    operations = [
        migrations.CreateModel(
            name='MesstoStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mess', models.TextField()),
                ('courseid', models.ForeignKey(to='teacherapp.Course_t')),
            ],
        ),
    ]
