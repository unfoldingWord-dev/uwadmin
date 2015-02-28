from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from .views import (
    api_contact,
    ContactList,
    ContactCreate,
    ContactDetail,
    ContactUpdate,
    OpenBibleStoryListView,
    OpenBibleStoryCreateView,
    OpenBibleStoryDetailView
)


urlpatterns = patterns(
    "",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^api/contacts/", api_contact, name="api_contacts"),
    url(r"^contacts/$", ContactList.as_view(), name="contact_list"),
    url(r"^contacts/create/$", ContactCreate.as_view(), name="contact_create"),
    url(r"^contacts/(?P<pk>\d+)/$", ContactDetail.as_view(), name="contact_detail"),
    url(r"^contacts/(?P<pk>\d+)/update/$", ContactUpdate.as_view(), name="contact_update"),
    url(r"^obs/$", OpenBibleStoryListView.as_view(), name="obs_list"),
    url(r"^obs/create/$", OpenBibleStoryCreateView.as_view(), name="obs_create"),
    url(r"^obs/(?P<pk>\d+)/$", OpenBibleStoryDetailView.as_view(), name="obs_detail"),
    url(r"^obs/(?P<code>[\w-]+)/update/$", OpenBibleStoryCreateView.as_view(), name="obs_update"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
