import os
import glob
import codecs
from django.core.exceptions import ObjectDoesNotExist
from uwadmin.models import Contact

door43users = '/var/www/vhosts/door43.org/httpdocs/conf/users.auth.php'
door43meta = '/var/www/vhosts/door43.org/httpdocs/data/meta/{0}/obs'

def getUsers(authfile):
    users = {}
    f = codecs.open(authfile, encoding='utf-8', mode='r')
    for line in f.readlines():
        # login:passwordhash:Real Name:email:groups,comma,seperated
        if line.startswith('#') or line.startswith('\n'):
            continue
        parts = line.split(':')
        if parts[0] == '':
            continue
        users[parts[0]] = { 'name': parts[2],
                            'email': parts[3],
                            'groups': parts[4]
                          }
    return users

def door43Sync():
    created = []
    users = getUsers(door43users)
    for k,v in users.iteritems():
       obj, crtd = Contact.objects.get_or_create(d43username=k)
       if crtd:
           obj.name = v['name']
           obj.email = v['email']
           obj.other = u'Door43 Groups: {0}'.format(v['groups'])
           obj.save()
           created.append(k)
    return created

def getContrib(lang):
    metadir = door43meta.format(lang)
    users = []
    for filename in glob.glob(os.path.join(metadir, '[0-5][0-9]*.changes')):
        f = codecs.open(filename, encoding='utf-8', mode='r')
        for line in f.readlines():
            if line.startswith('#') or line.startswith('\n'):
                continue
            user = line.split()[4]
            if user in [ 'admin', 'editor' ]:
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
