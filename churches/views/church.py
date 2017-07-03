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


class ChurchAdminMixin(LoginRequiredMixin):
    model = Church

    def dispatch(self, request, *args, **kwargs):
        self.church = get_object_or_404(
            Church,
            slug=self.kwargs.get("slug"),
            memberships__user=self.request.user,
            memberships__permission__lt=3
        )
        self.membership = self.church.memberships.get(user=self.request.user)
        return super(ChurchAdminMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChurchAdminMixin, self).get_context_data(**kwargs)
        context['church'] = self.church
        context['is_owner'] = self.membership.permission == 1
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


class ChurchMembershipUpdateView(ChurchAdminMixin, UpdateView):
    model = ChurchMembership
    fields = ['title', 'permission']
    template_name = "churches/membership_update.html"

    def get_queryset(self):
        return super(ChurchMembershipUpdateView, self).get_queryset().filter(
            church=self.church)

    def get_success_url(self):
        return reverse('church-membership-list', kwargs={'slug': self.church.slug})
