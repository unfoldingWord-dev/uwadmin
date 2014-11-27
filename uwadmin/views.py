from django.utils import timezone
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from uwadmin.models import *


class ContactList(ListView):
    model = Contact
    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        context = super(ContactList, self).get_context_data(**kwargs)
        return context

class ContactDetail(DetailView):
    model = Contact
    template_name = 'contact_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContactDetail, self).get_context_data(**kwargs)
        return context

def Tracking(request):
    pass

def Publishing(request):
    pass
