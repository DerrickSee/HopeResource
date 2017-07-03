from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.core.urlresolvers import reverse

from saleor.dashboard.views import staff_member_required
from saleor.userprofile.forms import get_address_form

from ..models import *
from ..forms import *


class ChurchMixin(object):
    model = Church
    form_class = ChurchForm


class ChurchListView(ChurchMixin, ListView):
    template_name = "dashboard/churches/church_list.html"


class ChurchCreateView(ChurchMixin, CreateView):
    template_name = "dashboard/churches/church_form.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ChurchCreateView, self).get_context_data(*args, **kwargs)
        context['address_form'], preview = get_address_form(
            None, initial={'country': self.request.country},
            country_code=self.request.country.code)
        return context

    def get_success_url(self):
        return reverse('dashboard:church-list')


class ChurchDetailView(ChurchMixin, UpdateView):
    template_name = "dashboard/churches/church_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ChurchDetailView, self).get_context_data(**kwargs)
        context['membership_form'] = ChurchMembershipForm()
        return context

    def get_success_url(self):
        return reverse('dashboard:church-detail', kwargs={'pk': self.object.pk})


class ChurchMembershipCreateView(ChurchMixin, CreateView):
    form_class = ChurchMembershipForm

    def form_valid(self, form):
        church = get_object_or_404(Church, pk=self.kwargs.get('pk'))
        membership = church.memberships.filter(user__email=form.cleaned_data['email']).first()
        if membership:
            form.instance.pk = membership.pk
            form.instance.date_joined = membership.date_joined
        form.instance.church = church
        form.save()
        return super(ChurchMembershipCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dashboard:church-detail', kwargs={'pk': self.object.church.pk}) + "#membership"
