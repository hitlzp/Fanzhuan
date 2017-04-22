# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacherapp', '0001_initial'),
        ('commonapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inclass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('command', models.CharField(max_length=100)),
                ('courseid', models.ForeignKey(to='teacherapp.Course_t')),
            ],
        ),
    ]
