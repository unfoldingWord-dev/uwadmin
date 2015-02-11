from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from .views import (
    ApiContact,
    ContactList,
    ContactCreate,
    ContactDetail,
    ContactUpdate,
    PubAll,
    PubLang,
    TrackAll,
    TrackLang
)


urlpatterns = patterns(
    "",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^api/contacts/", ApiContact.as_view(), name="api_contacts"),
    url(r"^contacts/$", ContactList.as_view(), name="contact_list"),
    url(r"^contacts/create/$", ContactCreate.as_view(), name="contact_create"),
    url(r"^contacts/(\d+)/$", ContactDetail.as_view(), name="contact_detail"),
    url(r"^contacts/(?P<pk>\d+)/update/$", ContactUpdate.as_view(), name="contact_update"),
    url(r"^publish/$", PubAll.as_view(), name="publish_all"),
    url(r"^publish/([\w-]+)/$", PubLang.as_view(), name="publish_language"),
    url(r"^track/$", TrackAll.as_view(), name="track_all"),
    url(r"^track/([\w-]+)/$", TrackLang.as_view(), name="track_language"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
