from __future__ import absolute_import

import subprocess
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from celery import task
from .models import PublishRequest


@task()
def publish(langcode):
    subprocess.call(["/var/www/vhosts/door43.org/tools/uw/publish.sh", "-l", langcode])


@task()
def send_request_email(request_id):
    pr = PublishRequest.objects.get(pk=request_id)
    html_contents = render_to_string("./uwadmin/email_html_publishrequest.html", {"publish_request": pr})
    plain_contents = render_to_string("./uwadmin/email_plain_publishrequest.html", {"publish_request": pr})
    send_mail("Publish Request #{0}".format(str(pr.pk)),
              plain_contents,
              settings.EMAIL_FROM,
              settings.EMAIL_NOTIFY_LIST,
              html_message=html_contents)
