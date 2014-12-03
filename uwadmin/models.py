from django.db import models
from django.contrib.auth.models import User

CHECKING_LEVEL_CHOICES = (
  (1, '1'),
  (2, '2'),
  (3, '3'),
)


class LangCode(models.Model):
    langcode = models.CharField(max_length=25, unique=True,
        help_text="Language Code.")
    langname = models.CharField(max_length=255,
        help_text="Name of language.")
    class Meta:
        ordering = ('langcode',)
    def __unicode__(self):
        return self.langcode

class Contact(models.Model):
    name = models.CharField(max_length=255,
        verbose_name="Name of contact")
    email = models.CharField(max_length=255, blank=True,
        verbose_name="Email address")
    d43username = models.CharField(max_length=255, blank=True,
        verbose_name="Door43 username")
    location = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True,
        verbose_name="Phone number")
    languages = models.ManyToManyField(LangCode, related_name="Contact")
    relationship = models.CharField(max_length=255, blank=True)
    other = models.CharField(max_length=255, blank=True,
        verbose_name="Other information")
    checking_entity = models.BooleanField(default=False)
    class Meta:
        ordering = ('name',)
    def __unicode__(self):
        return self.name

class RecentCommunication(models.Model):
    contact = models.ForeignKey(Contact, related_name="RecentCommunication",
        help_text="Name of contact.")
    communication = models.TextField(blank=True, verbose_name="Message")
    created = models.DateTimeField(auto_now_add=True,
        help_text="Time when entry was added.")
    created_by = models.ForeignKey(User,
        help_text="User who added this entry.")
    class Meta:
        ordering = ('contact', 'created')
    def __unicode__(self):
        return self.contact.name

class OBSTracking(models.Model):
    lang = models.ForeignKey(LangCode, related_name="OBSTracking",
        verbose_name="Language.")
    contact = models.ForeignKey(Contact, related_name="OBSTracking")
    date_started = models.DateField()
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    class Meta:
        ordering = ('lang', 'contact')
    def __unicode__(self):
        return self.lang.langcode

class OBSPublishing(models.Model):
    lang = models.ForeignKey(LangCode, related_name="OBSPublishing",
        help_text="Language code.")
    publish_date = models.DateField()
    version = models.CharField(max_length=10, help_text="Version of text.")
    source_text = models.ForeignKey(LangCode,
        help_text="Source text language code.")
    source_version = models.CharField(max_length=10, 
        help_text="Source text version.")
    checking_entity = models.ManyToManyField(Contact,
        related_name="OBSPublishing",
        help_text="Checking entities for this translation.")
    contributors = models.ManyToManyField(Contact,
        help_text="List of door43 usernames.")
    checking_level = models.IntegerField(choices=CHECKING_LEVEL_CHOICES)
    comments = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
        help_text="User who added this entry.")
    class Meta:
        ordering = ('lang',)
    def __unicode__(self):
        return self.lang.langcode
