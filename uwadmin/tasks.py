from __future__ import absolute_import

import subprocess

from django.db import connection

from celery import task


@task()
def publish(langcode):
    subprocess.call(["/var/www/vhosts/door43.org/tools/uw/publish.sh", "-l", langcode])
