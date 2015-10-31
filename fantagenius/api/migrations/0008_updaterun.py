# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_player_penalties_scored'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('duration', models.FloatField()),
                ('no_new_votes', models.IntegerField(default=0)),
                ('no_new_players', models.IntegerField(default=0)),
                ('no_new_orphans', models.IntegerField(default=0)),
            ],
        ),
    ]
