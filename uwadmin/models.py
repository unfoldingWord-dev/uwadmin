from django.db import models

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
    name = models.CharField(max_length=255, unique=True,
        help_text="Name of language.")
    email = models.CharField(max_length=255, blank=True,
        help_text="Email address.")
    d43username = models.CharField(max_length=255, blank=True,
        help_text="Door43 username.")
    location = models.CharField(max_length=255, blank=True,
        help_text="Location.")
    phone = models.CharField(max_length=255, blank=True,
        help_text="Phone number.")
    languages = models.ManyToManyField(LangCode,
        related_name="Contact",
        help_text="Langauges spoken by contact.")
    relationship = models.TextField(blank=True,
        help_text="Relationships to other people or organizations.")
    other = models.CharField(max_length=255, blank=True,
        help_text="Other information.")
    checking_entity = models.BooleanField(default=False,
        help_text="Is this a checking entity?")
    class Meta:
        ordering = ('name',)
    def __unicode__(self):
        return self.name

class RecentCommunication(models.Model):
    contact = models.ForeignKey(Contact, related_name="RecentCommunication",
        help_text="Name of contact.")
    communication = models.TextField(blank=True, help_text="Communication.")
    created = models.DateField(auto_now_add=True,
        help_text="Time when entry was added.")
    created_by = models.CharField(max_length=50,
        help_text="User who added this entry.")
    class Meta:
        ordering = ('contact', 'created')
    def __unicode__(self):
        return self.contact.name

class OBSTracking(models.Model):
    lang = models.ForeignKey(LangCode, related_name="OBSTracking",
        help_text="Language code.")
    contact = models.ForeignKey(Contact, related_name="OBSTracking",
        help_text="Contact for this project.")
    date_started = models.DateField(help_text="Date translation was started.")
    notes = models.TextField(blank=True, help_text="Notes.")
    created = models.DateField(auto_now_add=True,
        help_text="Time when entry was added.")
    last_modified = models.DateTimeField(auto_now=True,
        help_text="Time when entry was last modified.")
    created_by = models.CharField(max_length=50,
        help_text="User who added this entry.")
    updated_by = models.CharField(max_length=50,
        help_text="User who last updated this entry.")
    class Meta:
        ordering = ('lang', 'contact')
    def __unicode__(self):
        return self.lang.langcode

class OBSPublishing(models.Model):
    lang = models.ForeignKey(LangCode, related_name="OBSPublishing",
        help_text="Language code.")
    publish_date = models.DateField(help_text="Date translation was started.")
    version = models.CharField(max_length=10, help_text="Version of text.")
    source_text = models.ForeignKey(LangCode,
        help_text="Source text language code.")
    source_version = models.CharField(max_length=10, 
        help_text="Source text version.")
    checking_entity = models.ManyToManyField(Contact,
        related_name="OBSPublishing",
        help_text="Checking entities for this translation.")
    contributors = models.CharField(max_length=255,
        help_text="List of door43 usernames.")
    checking_level = models.IntegerField()
    comments = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,
        help_text="Time when entry was added.")
    last_modified = models.DateTimeField(auto_now=True,
        help_text="Time when entry was last modified.")
    created_by = models.CharField(max_length=50,
        help_text="User who added this entry.")
    updated_by = models.CharField(max_length=50,
        help_text="User who last updated this entry.")
    class Meta:
        ordering = ('lang',)
    def __unicode__(self):
        return self.lang.langcode
