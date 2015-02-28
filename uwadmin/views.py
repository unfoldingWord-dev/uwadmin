from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from django.contrib import messages

from account.decorators import login_required
from account.mixins import LoginRequiredMixin

from .models import Contact, OpenBibleStory, LangCode
from .forms import RecentComForm, ConnectionForm, OpenBibleStoryForm


@login_required
def api_contact(request):
    q = request.GET.get("term", "")
    data = [
        dict(
            id=o.pk,
            label=o.name,
            value=o.pk,
            url=reverse("contact_detail", args=[o.pk])
        )
        for o in Contact.objects.filter(name__icontains=q)[:10]
    ]
    return JsonResponse(data, safe=False)


class ContactList(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contacts.html"


class ContactDetail(LoginRequiredMixin, DetailView):
    template_name = "contact_detail.html"
    model = Contact

    def get_context_data(self, **kwargs):
        context = super(ContactDetail, self).get_context_data(**kwargs)
        context.update({
            "form_com": RecentComForm(user=self.request.user, contact=self.object),
            "recent_coms": self.object.recent_communications.all().order_by("-created"),
            "form_con": ConnectionForm(contact=self.object),
            "connections": self.object.source_connections.all().order_by("con_type")
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print self.object
        print request.user
        print request.POST
        context = self.get_context_data(object=self.object)
        if "recent_com" in request.POST:
            form_com = RecentComForm(
                request.POST,
                user=request.user,
                contact=self.object
            )
            if form_com.is_valid():
                form_com.save()
                messages.info(request, "Entry added.")
                return redirect("contact_detail", self.object.pk)
            else:
                context["form_com"] = form_com
        if "con" in request.POST:
            form_con = ConnectionForm(request.POST, contact=self.object)
            if form_con.is_valid():
                form_con.save()
                messages.info(request, "Connection created.")
                return redirect("contact_detail", self.object.pk)
            else:
                context["form_con"] = ConnectionForm(contact=self.object)
        return self.render_to_response(context)


class ContactMixin(LoginRequiredMixin):
    model = Contact
    fields = ["name", "email", "d43username", "location", "phone", "languages", "org", "other"]

    def get_success_url(self):
        return reverse("contact_detail", args=[self.object.pk])


class ContactUpdate(ContactMixin, UpdateView):
    template_name = "contact_update.html"


class ContactCreate(ContactMixin, CreateView):
    template_name = "contact_create.html"


class OpenBibleStoryCreateView(LoginRequiredMixin, CreateView):
    form_class = OpenBibleStoryForm
    model = OpenBibleStory

    def get_success_url(self):
        return reverse("obs_list")

    @property
    def lang(self):
        if not hasattr(self, "_lang"):
            if self.kwargs.get("code"):
                self._lang = get_object_or_404(LangCode, langcode=self.kwargs.get("code"))
            else:
                self._lang = None
        return self._lang

    def get_context_data(self, **kwargs):
        context = super(OpenBibleStoryCreateView, self).get_context_data(**kwargs)
        if self.lang:
            context.update(dict(lang=self.lang))
        return context

    def get_form(self, form_class):
        form = super(OpenBibleStoryCreateView, self).get_form(form_class)
        if self.lang:
            del form.fields["lang"]
        return form

    def get_initial(self):
        initial = super(OpenBibleStoryCreateView, self).get_initial()
        try:
            obs = OpenBibleStory.objects.filter(lang=self.lang).latest("created")
            initial.update(dict(
                contact=obs.contact,
                date_started=obs.date_started,
                notes=obs.notes,
                offline=obs.offline,
                publish_date=obs.publish_date,
                version=obs.version,
                source_text=obs.source_text,
                source_version=obs.source_version,
                checking_entity=obs.checking_entity.all(),
                checking_level=obs.checking_level
            ))
            print initial
        except OpenBibleStory.DoesNotExist:
            pass
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.lang:
            self.object.lang = self.lang
        self.object.created_by = self.request.user
        self.object.save()
        form.save_m2m()
        # @@@ Publish forms used to:
        # for contrib in get_contrib(self.lang):
        #     entry.contributors.add(contrib)
        return redirect(self.get_success_url())


class OpenBibleStoryListView(LoginRequiredMixin, ListView):
    model = OpenBibleStory

    def get_queryset(self, **kwargs):
        qs = super(OpenBibleStoryListView, self).get_queryset(**kwargs)
        qs = qs.order_by("lang__langname", "-created")
        return qs


class OpenBibleStoryDetailView(LoginRequiredMixin, DetailView):
    model = OpenBibleStory
