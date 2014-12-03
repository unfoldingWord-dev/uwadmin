import codecs
from uwadmin.models import Contact

door43users = '/var/www/vhosts/door43.org/httpdocs/conf/users.auth.php'

def getUsers(authfile):
    users = {}
    f = codecs.open(authfile, encoding='utf-8', mode='r')
    for line in f.readlines():
        # login:passwordhash:Real Name:email:groups,comma,seperated
        parts = line.split(':')
        if line.startswith('#') or line.startswith('\n'):
            continue
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
