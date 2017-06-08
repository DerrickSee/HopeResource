from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.core.urlresolvers import reverse

from saleor.dashboard.views import staff_member_required
from saleor.userprofile.forms import get_address_form

from .models import *
from .forms import *

# Create your views here.
class ChurchMixin(object):
    model = Church
    form_class = ChurchForm


class ChurchListView(ChurchMixin, ListView):
    pass


class ChurchCreateView(ChurchMixin, CreateView):

    def get_context_data(self, *args, **kwargs):
        context = super(ChurchCreateView, self).get_context_data(*args, **kwargs)
        context['address_form'], preview = get_address_form(
            None, initial={'country': self.request.country},
            country_code=self.request.country.code)
        return context

    def get_success_url(self):
        return reverse('dashboard:church-list')


class ChurchDetailView(ChurchMixin, UpdateView):
    template_name = "churches/church_detail.html"

    def get_success_url(self):
        return reverse('dashboard:church-detail', kwargs={'pk': self.object.pk})
