# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20151020_1204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='sub_in',
        ),
        migrations.RemoveField(
            model_name='player',
            name='sub_out',
        ),
        migrations.AddField(
            model_name='vote',
            name='sub_in',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vote',
            name='sub_out',
            field=models.BooleanField(default=False),
        ),
    ]
