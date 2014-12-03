import json
import urllib2
from uwadmin.models import LangCode

lang_url = 'http://td.unfoldingword.org/exports/langnames.json'


def getLangs(url):
    try:
        request = urllib2.urlopen(url).read()
    except:
        request = '{}'
    return json.loads(request)

def tDSyncLangs():
    created = []
    lang_info = getLangs(lang_url)
    for l in lang_info:
       obj, crtd = LangCode.objects.get_or_create(langcode=l['lc'])
       if crtd:
           obj.langname = l['ln']
           obj.save()
           created.append(l['lc'])
    return created
