# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0005_messtostudent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messtostudent',
            name='courseid',
        ),
        migrations.DeleteModel(
            name='MesstoStudent',
        ),
    ]
