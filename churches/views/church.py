from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, CreateView, UpdateView, DetailView,
                                  TemplateView)
from django.core.urlresolvers import reverse

from saleor.dashboard.views import staff_member_required
from saleor.userprofile.forms import get_address_form

from ..models import *
from ..forms import *


class ChurchAdminMixin(object):
    model = Church


class ChurchHomeView(TemplateView):
    template_name = 'churches/base.html'


class ChurchMembershipListView(ListView):
    model = ChurchMembership

    def get_queryset(self):
        return super(ChurchMembershipListView, self).get_queryset().filter(
            church__slug=self.kwargs.get("slug")
        )
