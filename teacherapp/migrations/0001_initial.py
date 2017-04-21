# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cname', models.CharField(max_length=100)),
                ('sum', models.IntegerField(default=0)),
                ('recommend', models.TextField()),
                ('segmentsum', models.IntegerField(default=0)),
                ('groupsum', models.IntegerField(default=0)),
                ('starttime', models.DateTimeField(default=b'2017-01-01 00:00:00')),
                ('isvalid', models.IntegerField(default=0)),
                ('mytype', models.IntegerField(default=0)),
                ('teacher', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Segmnet_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sname', models.CharField(max_length=100, verbose_name=b'\xe7\x8e\xaf\xe8\x8a\x82\xe5\x90\x8d')),
                ('minute', models.IntegerField(default=0)),
                ('content', models.TextField()),
                ('ratio', models.IntegerField(default=0)),
                ('isvalid', models.IntegerField(default=0)),
                ('tcourse', models.ForeignKey(to='teacherapp.Course_t')),
            ],
        ),
        migrations.CreateModel(
            name='Table_t',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.IntegerField(default=0)),
                ('ratio', models.IntegerField(default=0)),
                ('tsegment', models.ForeignKey(to='teacherapp.Segmnet_t')),
            ],
        ),
    ]
