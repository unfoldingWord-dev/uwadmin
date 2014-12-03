from django.contrib import admin
from uwadmin.lang import *
from uwadmin.utils import *
from uwadmin.models import *


class LangCodeAdmin(admin.ModelAdmin):
    list_display = ('langcode', 'langname')
    list_display_links = ('langcode',)
    search_fields = ('langcode', 'langname')
    actions = ['tDSync']
    def tDSync(self, request, queryset):
        created = tDSyncLangs()
        self.message_user(request, 'Created: {0}'.format(created))
    tDSync.short_description = "tD Sync"

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'd43username', 'email', 'phone', 'other',
                                                            'checking_entity')
    list_display_links = ('name',)
    list_filter = ('checking_entity',)
    search_fields = ('name', 'email', 'phone', 'other')
    actions = ['D43Sync']
    def D43Sync(self, request, queryset):
        created = door43Sync()
        self.message_user(request, 'Created: {0}'.format(created))
    D43Sync.short_description = "Door43 User Sync"

class RecentCommunicationAdmin(admin.ModelAdmin):
    list_display = ('contact', 'communication', 'created', 'created_by')
    list_display_links = ('contact',)
    list_filter = ('contact', 'created', 'created_by')
    search_fields = ('contact', 'communication')

class OBSTrackingAdmin(admin.ModelAdmin):
    list_display = ('lang', 'contact', 'date_started', 'notes', 'created', 
        'created_by')
    list_display_links = ('lang',)
    list_editable = ('contact', 'notes')
    list_filter = ('contact', 'date_started')
    search_fields = ('contact', 'notes')

class OBSPublishingAdmin(admin.ModelAdmin):
    list_display = ('lang', 'publish_date', 'version',
        'checking_level', 'source_text', 'source_version',
        'comments', 'created_by')
    list_display_links = ('lang',)
    list_filter = ('checking_level', 'publish_date', 'version', 'source_text',
        'source_version')
    search_fields = ('lang', 'publish_date', 'version', 'checking_entity',
        'checking_level', 'contributors', 'source_text', 'source_version',
        'comments', 'created_by')

admin.site.register(LangCode, LangCodeAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(RecentCommunication, RecentCommunicationAdmin)
admin.site.register(OBSTracking, OBSTrackingAdmin)
admin.site.register(OBSPublishing, OBSPublishingAdmin)
