import json
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import *
from django.views.generic.edit import *
from django.views.generic.detail import *
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from .models import *
from .forms import *


class getContact(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(getContact, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        siteurl = 'http://96.126.122.51:9000{0}'
        if request.is_ajax():
            q = request.GET.get('term', '')
            objects = Contact.objects.filter(name__icontains=q)[:10]
            results = []
            for obj in objects:
                obj_json = {}
                obj_json['id'] = obj.id
                obj_json['label'] = obj.name
                #obj_json['value'] = 'http://' #{0}'.format(obj.id)
                obj_json['value'] = siteurl.format(reverse('contactdetail', args=[obj.id]))
                results.append(obj_json)
            data = json.dumps(results)
        else:
            data = 'fail'
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)


class ContactList(ListView):
    model = Contact
    template_name = 'contacts.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactList, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactList, self).get_context_data(**kwargs)
        return context


class ContactDetail(View):
    template_name = 'contact_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactDetail, self).dispatch(*args, **kwargs)

    def setup(self, request):
        self.contact = get_object_or_404(Contact, id=self.args[0])
        context = { 'object': self.contact }
        return context

    def get(self, request, *args, **kwargs):
        context = self.setup(request)
        context['form'] = RecentComForm(self.request.user, self.contact)
        context['recent_coms'] = RecentCommunication.objects.filter(
                               contact=self.args[0]).order_by('-created')
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.setup(request)
        form = RecentComForm(self.request.user, self.contact, request.POST)
        if form.is_valid():
            form.save()
            context['success'] = 'Entry added.'
            context['form'] = RecentComForm(self.request.user, self.args[0])
        else:
            context['form'] = form
        context['recent_coms'] = RecentCommunication.objects.filter(
                               contact=self.args[0]).order_by('-created')
        return render(request, self.template_name, context)


class ContactUpdate(UpdateView):
    model = Contact
    fields = ['name', 'email', 'd43username', 'location', 'phone', 'languages', 
                                  'relationship', 'other', 'checking_entity', ]
    template_name = 'contact_update.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactUpdate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('contactdetail', args=[self.object.pk])


class ContactCreate(CreateView):
    model = Contact
    fields = ['name', 'email', 'd43username', 'location', 'phone', 'languages', 
                                  'relationship', 'other', 'checking_entity', ]
    template_name = 'contact_create.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactCreate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('contactdetail', args=[self.object.pk])


class TrackAll(View):
    template_name = 'track_all.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TrackAll, self).dispatch(*args, **kwargs)

    def setup(self, request):
        entries = {}
        for x in OBSTracking.objects.all():
            if not entries.has_key(x.lang.langcode):
                entries[x.lang.langcode] = x.lang.langname
        return { 'object_list': entries }

    def get(self, request, *args, **kwargs):
        context = self.setup(request)
        context['form'] = LangTrackNewForm(self.request.user)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.setup(request)
        form = LangTrackNewForm(self.request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/track/{0}/'.format(
                                                   form.cleaned_data['lang']))
        else:
            context['form'] = form
            return render(request, self.template_name, context)


class TrackLang(View):
    template_name = 'track_lang.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TrackLang, self).dispatch(*args, **kwargs)

    def setup(self, request):
        self.lang = get_object_or_404(LangCode, langcode=self.args[0])
        object_list = OBSTracking.objects.filter(lang=self.lang)
        context = {'object_list': object_list}
        context['lang'] = self.lang
        return context

    def get(self, request, *args, **kwargs):
        context = self.setup(request)
        context['form'] = LangTrackForm(self.lang, self.request.user)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.setup(request)
        form = LangTrackForm(self.lang, self.request.user, request.POST)
        if form.is_valid():
            form.save()
            context['success'] = 'Entry added.'
            context['form'] = LangTrackForm(self.lang, self.request.user)
        else:
            context['form'] = form
        return render(request, self.template_name, context)


class PubAll(View):
    template_name = 'pub_all.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PubAll, self).dispatch(*args, **kwargs)

    def setup(self, request):
        entries = {}
        for x in OBSPublishing.objects.all().order_by('-publish_date'):
            if not entries.has_key(x.lang.langcode):
                entries[x.lang.langcode] = { 'name': x.lang.langname,
                                             'publish_date': x.publish_date,
                                             'version': x.version
                                           }
        return { 'object_list': entries }

    def get(self, request, *args, **kwargs):
        context = self.setup(request)
        context['form'] = LangPubNewForm(self.request.user)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.setup(request)
        form = LangPubNewForm(self.request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/publish/{0}/'.format(
                                                   form.cleaned_data['lang']))
        else:
            context['form'] = form
            return render(request, self.template_name, context)


class PubLang(View):
    template_name = 'pub_lang.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PubLang, self).dispatch(*args, **kwargs)

    def setup(self, request):
        self.lang = get_object_or_404(LangCode, langcode=self.args[0])
        object_list = OBSPublishing.objects.filter(lang=self.lang).order_by(
                                                             '-publish_date')
        context = {'object_list': object_list}
        context['lang'] = self.lang
        return context

    def get(self, request, *args, **kwargs):
        context = self.setup(request)
        context['form'] = LangPubForm(self.lang, self.request.user)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.setup(request)
        form = LangPubForm(self.lang, self.request.user, request.POST)
        if form.is_valid():
            form.save()
            context['success'] = 'Entry added.'
            context['form'] = LangPubForm(self.lang, self.request.user)
        else:
            context['form'] = form
        return render(request, self.template_name, context)
