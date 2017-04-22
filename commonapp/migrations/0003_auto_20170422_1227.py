# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0002_inclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='inclass',
            name='isvalue',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inclass',
            name='segment',
            field=models.IntegerField(default=0),
        ),
    ]
