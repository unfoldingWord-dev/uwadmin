# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uwadmin', '0004_auto_20150227_1958'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OBSPublishing',
        ),
        migrations.DeleteModel(
            name='OBSTracking',
        ),
    ]
