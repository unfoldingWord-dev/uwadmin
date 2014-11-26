from django.shortcuts import render


def Contacts(request):
    '''
    List of contacts.
    '''
    content = { 'content': Contact.objects.all().order_by('name') }
    return render(request, 'uwadmin/contacts.html', content)

def Contact(request, cid):
    '''
    Detail for a specific contact.
    '''
    pass

def Tracking(request):
    pass

def Publishing(request):
    pass
