from django.forms import *
from .models import *
from .utils import *


class RecentComForm(ModelForm):
    class Meta:
        model = RecentCommunication
        fields = [ 'communication', ]
        widgets = {
            'communication': Textarea(attrs={'cols': 80, 'rows': 2}),
        }

    def __init__(self,  user, contact, *args, **kwargs):
        self.created_by = user
        self.contact = contact
        super(RecentComForm, self).__init__(*args, **kwargs)

    def save(self):
        entry = super(RecentComForm, self).save(commit=False)
        entry.created_by = self.created_by
        entry.contact = self.contact
        entry.save()


class LangTrackNewForm(ModelForm):
    class Meta:
        model = OBSTracking
        fields = ['lang', 'contact', 'date_started', 'notes']
        widgets = {
            'date_started': DateInput(attrs={'class':'datepicker'}),
        }

    def __init__(self,  user, *args, **kwargs):
        self.created_by = user
        super(LangTrackNewForm, self).__init__(*args, **kwargs)

    def save(self):
        entry = super(LangTrackNewForm, self).save(commit=False)
        entry.created_by = self.created_by
        entry.save()

class LangTrackForm(ModelForm):
    class Meta:
        model = OBSTracking
        fields = ['contact', 'date_started', 'notes']
        widgets = {
            'date_started': DateInput(attrs={'class':'datepicker'}),
        }

    def __init__(self, lang, user, *args, **kwargs):
        self.created_by = user
        self.lang = lang
        super(LangTrackForm, self).__init__(*args, **kwargs)

    def save(self):
        entry = super(LangTrackForm, self).save(commit=False)
        entry.lang = self.lang
        entry.created_by = self.created_by
        entry.save()

class LangPubForm(ModelForm):
    class Meta:
        model = OBSPublishing
        fields = [ 'publish_date', 'version', 'source_text', 'source_version',
                             'checking_entity', 'checking_level', 'comments' ]
        widgets = {
            'publish_date': DateInput(attrs={'class':'datepicker'}),
            'comments': Textarea(attrs={'rows': 2}),
        }

    def __init__(self, lang, user, *args, **kwargs):
        self.created_by = user
        self.lang = lang
        super(LangPubForm, self).__init__(*args, **kwargs)
        self.fields['checking_entity'].queryset = Contact.objects.filter(
                                                         checking_entity=True)

    def save(self):
        entry = super(LangPubForm, self).save(commit=False)
        entry.lang = self.lang
        entry.created_by = self.created_by
        entry.save()
        for contrib in getContrib(self.lang):
            entry.contributors.add(contrib)

class LangPubNewForm(ModelForm):
    class Meta:
        model = OBSPublishing
        fields = [ 'lang', 'publish_date', 'version', 'source_text',
                   'source_version', 'checking_entity', 'checking_level',
                                                                  'comments' ]
        widgets = {
            'publish_date': DateInput(attrs={'class':'datepicker'}),
            'comments': Textarea(attrs={'rows': 2}),
        }

    def __init__(self, user, *args, **kwargs):
        self.created_by = user
        super(LangPubNewForm, self).__init__(*args, **kwargs)
        self.fields['checking_entity'].queryset = Contact.objects.filter(
                                                         checking_entity=True)

    def save(self):
        entry = super(LangPubNewForm, self).save(commit=False)
        entry.created_by = self.created_by
        entry.save()
        for contrib in getContrib(entry.lang.langcode):
            entry.contributors.add(contrib)
