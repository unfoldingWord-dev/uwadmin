from django import forms

from .models import RecentCommunication, Connection, OpenBibleStory


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

    def __init__(self, *args, **kwargs):
        super(OpenBibleStoryForm, self).__init__(*args, **kwargs)
        self.fields["language"].queryset = self.fields["language"].queryset.filter(checking_level=3)
        self.fields["source_text"].queryset = self.fields["source_text"].queryset.filter(checking_level=3)

    class Meta:
        model = OpenBibleStory
        fields = [
            "language",
            "contact",
            "date_started",
            "notes",
            "offline",
            "publish_date",
            "version",
            "source_text",
            "source_version",
            "checking_entity",
            "checking_level"
        ]
