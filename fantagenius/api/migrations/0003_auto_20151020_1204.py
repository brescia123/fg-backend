# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20151018_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='sub_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='player',
            name='sub_out',
            field=models.BooleanField(default=False),
        ),
    ]
