# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_updaterun'),
    ]

    operations = [
        migrations.RenameField(
            model_name='updaterun',
            old_name='date',
            new_name='run_date',
        ),
    ]
