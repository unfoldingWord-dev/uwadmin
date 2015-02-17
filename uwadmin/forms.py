from django import forms

from .models import RecentCommunication, Connection, OBSTracking, OBSPublishing, Organization
from .utils import get_contrib


class RecentComForm(forms.ModelForm):
    class Meta:
        model = RecentCommunication
        fields = ["communication"]
        widgets = {
            "communication": forms.Textarea(attrs={
                "class": "form-control",
                "cols": 40,
                "rows": 2
            }),
        }

    def __init__(self, *args, **kwargs):
        self.created_by = kwargs.pop("user")
        self.contact = kwargs.pop("contact")
        super(RecentComForm, self).__init__(*args, **kwargs)

    def save(self):
        entry = super(RecentComForm, self).save(commit=False)
        entry.created_by = self.created_by
        entry.contact = self.contact
        entry.save()


class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ["con_dst", "con_type"]
        widgets = {
            "con_dst": forms.TextInput(attrs={
                "class": "form-control",
                "id": "contacts-id",
                "placeholder": "Add connection..."
            }),
        }

    def __init__(self, *args, **kwargs):
        self.contact = kwargs.pop("contact")
        super(ConnectionForm, self).__init__(*args, **kwargs)

    def save(self):
        entry = super(ConnectionForm, self).save(commit=False)
        entry.con_src = self.contact
        entry.save()
        if entry.con_type.mutual:
            Connection.objects.create(
                con_src=entry.con_dst,
                con_dst=self.contact,
                con_type=entry.con_type
            )


class LangTrackNewForm(forms.ModelForm):
    class Meta:
        model = OBSTracking
        fields = ["lang", "contact", "date_started", "notes"]
        widgets = {
            "contact": forms.Select(attrs={"class": "form-control"}),
            "date_started": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "lang": forms.Select(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "cols": 20, "rows": 2}),
        }

    def __init__(self, user, *args, **kwargs):
        self.created_by = user
        super(LangTrackNewForm, self).__init__(*args, **kwargs)

    def save(self):
        entry = super(LangTrackNewForm, self).save(commit=False)
        entry.created_by = self.created_by
        entry.save()


class LangTrackForm(forms.ModelForm):
    class Meta:
        model = OBSTracking
        fields = ["contact", "date_started", "notes"]
        widgets = {
            "contact": forms.Select(attrs={"class": "form-control"}),
            "date_started": forms.DateInput(attrs={"class": "form-control datepicker"}),
            "lang": forms.Select(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "cols": 20, "rows": 2}),
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


class LangPubForm(forms.ModelForm):
    class Meta:
        model = OBSPublishing
        fields = ["publish_date", "version", "source_text", "source_version", "checking_entity", "checking_level", "comments"]
        widgets = {
            "publish_date": forms.DateInput(attrs={"class": "form-control datepicker", "size": "8"}),
            "comments": forms.Textarea(attrs={"class": "form-control", "cols": 20, "rows": 2}),
            "version": forms.TextInput(attrs={"class": "form-control", "size": "5"}),
            "source_version": forms.TextInput(attrs={"class": "form-control", "size": "5"}),
            "checking_entity": forms.CheckboxSelectMultiple(),
            "checking_level": forms.Select(attrs={"class": "form-control"}),
            "source_text": forms.Select(attrs={"class": "form-control"}),
            "lang": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, lang, user, *args, **kwargs):
        self.created_by = user
        self.lang = lang
        super(LangPubForm, self).__init__(*args, **kwargs)
        self.fields["checking_entity"].queryset = Organization.objects.filter(checking_entity=True)

    def save(self):
        entry = super(LangPubForm, self).save(commit=False)
        entry.lang = self.lang
        entry.created_by = self.created_by
        entry.save()
        for contrib in get_contrib(self.lang):
            entry.contributors.add(contrib)


class LangPubNewForm(forms.ModelForm):
    class Meta:
        model = OBSPublishing
        fields = ["lang", "publish_date", "version", "source_text", "source_version", "checking_entity", "checking_level", "comments"]
        widgets = {
            "publish_date": forms.DateInput(attrs={"class": "form-control datepicker", "size": "8"}),
            "comments": forms.Textarea(attrs={"class": "form-control", "cols": 20, "rows": 2}),
            "version": forms.TextInput(attrs={"class": "form-control", "size": "5"}),
            "source_version": forms.TextInput(attrs={"class": "form-control", "size": "5"}),
            "checking_entity": forms.CheckboxSelectMultiple(),
            "checking_level": forms.Select(attrs={"class": "form-control"}),
            "source_text": forms.Select(attrs={"class": "form-control"}),
            "lang": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, user, *args, **kwargs):
        self.created_by = user
        super(LangPubNewForm, self).__init__(*args, **kwargs)
        self.fields["checking_entity"].queryset = Organization.objects.filter(checking_entity=True)

    def save(self):
        entry = super(LangPubNewForm, self).save(commit=False)
        entry.created_by = self.created_by
        entry.save()
        for contrib in get_contrib(entry.lang.langcode):
            entry.contributors.add(contrib)
