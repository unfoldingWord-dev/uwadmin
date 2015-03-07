from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

import requests


class LangCode(models.Model):
    langcode = models.CharField(max_length=25, unique=True, verbose_name="Language Code")
    langname = models.CharField(max_length=255, verbose_name="Language Name")
    checking_level = models.IntegerField(null=True)

    @classmethod
    def update_checking_levels(cls):
        catalog = requests.get("https://api.unfoldingword.org/obs/txt/1/obs-catalog.json").json()
        for lang in catalog:
            cls.objects.filter(langcode=lang["language"]).update(checking_level=lang["status"]["checking_level"])

    @classmethod
    def sync(cls):
        data = requests.get("http://td.unfoldingword.org/exports/langnames.json").json()
        for lang in data:
            cls.objects.get_or_create(langcode=lang["lc"], defaults={"langname": lang["ln"]})

    class Meta:
        ordering = ["langcode"]

    def __unicode__(self):
        return self.langcode


class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name of Organization")
    email = models.CharField(max_length=255, blank=True, verbose_name="Email address")
    phone = models.CharField(max_length=255, blank=True, verbose_name="Phone number")
    website = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    languages = models.ManyToManyField(LangCode, related_name="organizations")
    other = models.TextField(blank=True, verbose_name="Other information")
    checking_entity = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name of contact")
    email = models.CharField(max_length=255, blank=True, verbose_name="Email address")
    d43username = models.CharField(max_length=255, blank=True, verbose_name="Door43 username")
    location = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True, verbose_name="Phone number")
    languages = models.ManyToManyField(LangCode, related_name="contacts")
    org = models.ManyToManyField(Organization, blank=True, null=True, verbose_name="organizations")
    other = models.TextField(blank=True, verbose_name="Other information")

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name


class ConnectionType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name of Connection Type")
    mutual = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name


class Connection(models.Model):
    con_src = models.ForeignKey(Contact, related_name="source_connections")
    con_dst = models.ForeignKey(Contact, related_name="destination_connections", verbose_name="Connection")
    con_type = models.ForeignKey(ConnectionType, verbose_name="Type")

    class Meta:
        ordering = ["con_src"]

    def __unicode__(self):
        return self.con_src.name


class RecentCommunication(models.Model):
    contact = models.ForeignKey(Contact, related_name="recent_communications")
    communication = models.TextField(blank=True, verbose_name="Message")
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)

    class Meta:
        ordering = ["contact", "created"]

    def __unicode__(self):
        return self.contact.name


class OpenBibleStory(models.Model):
    CHECKING_LEVEL_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
    ]

    # Base + Tracking
    lang = models.ForeignKey(LangCode, related_name="resources", verbose_name="Language.")
    contact = models.ForeignKey(Contact, related_name="resources")
    date_started = models.DateField()
    notes = models.TextField(blank=True)
    offline = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User)

    # Publishing
    publish_date = models.DateField(null=True, blank=True)
    version = models.CharField(max_length=10, blank=True)
    source_text = models.ForeignKey(LangCode, null=True, blank=True, related_name="+")
    source_version = models.CharField(max_length=10, blank=True)
    checking_entity = models.ManyToManyField(Contact, related_name="resource_publications", blank=True)
    contributors = models.ManyToManyField(Contact, related_name="+", blank=True)
    checking_level = models.IntegerField(choices=CHECKING_LEVEL_CHOICES, null=True, blank=True)

    class Meta:
        ordering = ["lang", "contact"]

    def __unicode__(self):
        return self.lang.langcode


class Comment(models.Model):
    open_bible_story = models.ForeignKey(OpenBibleStory, related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User)
