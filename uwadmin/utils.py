import codecs
import glob
import os

from django.core.exceptions import ObjectDoesNotExist

from .models import Contact


door43_meta = "/var/www/vhosts/door43.org/httpdocs/data/meta/{0}/obs"


def get_contrib(lang):
    metadir = door43_meta.format(lang)
    users = []
    for filename in glob.glob(os.path.join(metadir, "[0-5][0-9]*.changes")):
        f = codecs.open(filename, encoding="utf-8", mode="r")
        for line in f.readlines():
            if line.startswith("#") or line.startswith("\n"):
                continue
            user = line.split()[4]
            if user in ["admin", "editor"]:
                continue
            if user not in users:
                users.append(user)
    contributors = []
    for user in set(users):
        try:
            obj = Contact.objects.get(d43username=user)
        except ObjectDoesNotExist:
            continue
        contributors.append(obj)
    return contributors
