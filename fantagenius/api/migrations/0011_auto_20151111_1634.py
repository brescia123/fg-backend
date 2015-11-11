# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20151031_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 11, 16, 34, 0, 857960, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 11, 16, 34, 2, 778593, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 11, 16, 34, 4, 714631, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 11, 16, 34, 8, 529288, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 11, 16, 34, 11, 962527, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 11, 16, 34, 13, 865293, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
