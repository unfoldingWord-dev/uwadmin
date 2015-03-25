from django import forms
from django.core.urlresolvers import reverse

from multiupload.fields import MultiFileField

from .models import RecentCommunication, Connection, OpenBibleStory, PublishRequest, LangCode


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


class OpenBibleStoryForm(forms.ModelForm):

    publish = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(OpenBibleStoryForm, self).__init__(*args, **kwargs)
        self.fields["language"].queryset = self.fields["language"].queryset.filter(checking_level=3)
        self.fields["source_text"].queryset = self.fields["source_text"].queryset.filter(checking_level=3)
        if self.instance.publish_date:
            self.fields["publish"].initial = True

    class Meta:
        model = OpenBibleStory
        fields = [
            "language",
            "contact",
            "date_started",
            "notes",
            "offline",
            "publish",
            "version",
            "source_text",
            "source_version",
            "checking_entity",
            "checking_level"
        ]


class PublishRequestForm(forms.ModelForm):

    license_agreements = MultiFileField(min_num=1, max_file_size=1024*1024*5)

    def __init__(self, *args, **kwargs):
        super(PublishRequestForm, self).__init__(*args, **kwargs)
        self.fields["language"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": reverse("names_autocomplete")
                }
            ),
            required=True
        )
        if self.is_bound:
            lang = next(iter(LangCode.objects.filter(langcode=self.data["language"])), None)
            if lang:
                self.fields["language"].widget.attrs["data-lang-ln"] = lang.langname
                self.fields["language"].widget.attrs["data-lang-lc"] = lang.langcode
                self.fields["language"].widget.attrs["data-lang-gl"] = lang.gateway_flag

    def clean_language(self):
        lc = self.cleaned_data["language"]
        if lc:
            return LangCode.objects.get(langcode=lc)

    class Meta:
        model = PublishRequest
        fields = [
            "requestor",
            "resource",
            "language",
            "checking_level",
            "contributors",
            "license_agreements"
        ]
