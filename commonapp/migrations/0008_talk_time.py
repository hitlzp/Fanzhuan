# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0007_talk'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='time',
            field=models.DateTimeField(default=b'2017-01-01 00:00:00'),
        ),
    ]
