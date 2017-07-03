from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, CreateView, UpdateView, DetailView,
                                  TemplateView)
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q

from saleor.dashboard.views import staff_member_required
from saleor.userprofile.forms import get_address_form

from ..models import *
from ..forms import *


class ChurchAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Church

    def dispatch(self, request, *args, **kwargs):
        self.church = get_object_or_404(Church, slug=self.kwargs.get("slug"))
        return super(ChurchAdminMixin, self).dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.churchmembership_set.filter(
            Q(church__slug=self.kwargs.get("slug")),
            Q(is_owner=True) | Q(is_staff=True)).exists()

    def get_context_data(self, **kwargs):
        context = super(ChurchAdminMixin, self).get_context_data(**kwargs)
        context['church'] = self.church
        return context


class ChurchHomeView(ChurchAdminMixin, TemplateView):
    template_name = 'churches/base.html'


class ChurchMembershipListView(ChurchAdminMixin, ListView):
    model = ChurchMembership

    def get_queryset(self):
        return super(ChurchMembershipListView, self).get_queryset().filter(
            church__slug=self.kwargs.get("slug")
        )


class ChurchMembershipCreateView(ChurchAdminMixin, CreateView):
    model = ChurchMembership
    form_class = ChurchMembershipForm

    def form_valid(self, form):
        form.instance.church = self.church
        return super(ChurchMembershipCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('church-membership-list', kwargs={'slug': self.church.slug})
