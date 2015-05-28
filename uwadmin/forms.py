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
        self.fields["language"].queryset = self.fields["language"].queryset.all()
        self.fields["source_text"].queryset = self.fields["source_text"].queryset.filter(checking_level=3)
        if self.instance.publish_date:
            self.fields["publish"].initial = True
        if not self.fields["publish"].initial:
            self.fields["version"].widget.attrs["disabled"] = "disabled"
            self.fields["checking_entity"].widget.attrs["disabled"] = "disabled"
            self.fields["checking_level"].widget.attrs["disabled"] = "disabled"

    class Meta:
        model = OpenBibleStory
        fields = [
            "language",
            "contact",
            "date_started",
            "notes",
            "offline",
            "source_text",
            "source_version",
            "publish",
            "version",
            "checking_entity",
            "checking_level"
        ]


class PublishRequestForm(forms.ModelForm):

    license_agreements = MultiFileField(required=False, min_num=0, max_file_size=5242880)  # 5 MB

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
        self.fields["source_text"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": reverse("names_autocomplete")
                }
            ),
            required=True
        )
        if self.instance.pk:
            lang = self.instance.language
            if lang:
                self.fields["language"].widget.attrs["data-lang-ln"] = lang.langname
                self.fields["language"].widget.attrs["data-lang-lc"] = lang.langcode
                self.fields["language"].widget.attrs["data-lang-gl"] = lang.gateway_flag
            src_text = self.instance.source_text
            if src_text:
                self.fields["source_text"].widget.attrs["data-lang-ln"] = src_text.langname
                self.fields["source_text"].widget.attrs["data-lang-lc"] = src_text.langcode
                self.fields["source_text"].widget.attrs["data-lang-gl"] = src_text.gateway_flag

    def clean_language(self):
        lc = self.cleaned_data["language"]
        if lc:
            return LangCode.objects.get(langcode=lc)

    def clean_source_text(self):
        slc = self.cleaned_data["source_text"]
        if slc:
            return LangCode.objects.get(langcode=slc)

    class Meta:
        model = PublishRequest
        fields = [
            "requestor",
            "resource",
            "language",
            "source_text",
            "source_version",
            "checking_level",
            "contributors",
            "license_agreements"
        ]
