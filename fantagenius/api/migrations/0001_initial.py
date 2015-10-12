# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=1)),
                ('team', models.CharField(max_length=20)),
                ('price', models.IntegerField(default=1)),
                ('attendances', models.IntegerField(default=0)),
                ('gol', models.IntegerField(default=0)),
                ('assist', models.IntegerField(default=0)),
                ('yellow_cards', models.IntegerField(default=0)),
                ('red_cards', models.IntegerField(default=0)),
                ('penalties_kicked', models.IntegerField(default=0)),
                ('penalties_missed', models.IntegerField(default=0)),
                ('penalties_saved', models.IntegerField(default=0)),
                ('vote_avg', models.FloatField(default=0.0)),
                ('magicvote_avg', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.FloatField(default=0.0)),
                ('gol', models.IntegerField(default=0)),
                ('assist', models.IntegerField(default=0)),
                ('penalties_scored_saved', models.IntegerField(default=0)),
                ('penalties_missed', models.IntegerField(default=0)),
                ('own_gol', models.IntegerField(default=0)),
                ('yellow_cards', models.IntegerField(default=0)),
                ('red_cards', models.IntegerField(default=0)),
                ('magicvote', models.FloatField(default=0.0)),
                ('day', models.IntegerField(default=0)),
                ('player', models.ForeignKey(to='api.Player')),
            ],
        ),
    ]
