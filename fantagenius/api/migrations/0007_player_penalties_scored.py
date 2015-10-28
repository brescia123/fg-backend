# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20151020_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='penalties_scored',
            field=models.IntegerField(default=0),
        ),
    ]
