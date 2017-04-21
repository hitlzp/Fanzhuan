# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teacherapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.IntegerField(default=0)),
                ('grade', models.FloatField(default=0)),
                ('course', models.ForeignKey(to='teacherapp.Course_t')),
                ('stu', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='User_class',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clas', models.IntegerField(default=0)),
                ('person', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
