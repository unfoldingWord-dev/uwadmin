# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uwadmin', '0005_auto_20150227_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='langcode',
            name='checking_level',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
