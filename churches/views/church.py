from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, CreateView, UpdateView, DetailView,
                                  TemplateView, DeleteView)
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from saleor.dashboard.views import staff_member_required
from saleor.userprofile.forms import get_address_form
from saleor.product.models import Product

from ..models import *
from ..forms import *


class ChurchAdminMixin(LoginRequiredMixin):
    model = Church
    permission = 2

    def dispatch(self, request, *args, **kwargs):
        self.church = get_object_or_404(
            Church,
            slug=self.kwargs.get("slug"),
            memberships__user=self.request.user,
            memberships__permission__lte=self.permission
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


class ChurchAdminMembershipMixin(ChurchAdminMixin):
    model = ChurchMembership

    def get_queryset(self):
        return super(ChurchAdminMembershipMixin, self).get_queryset().filter(
            church=self.church)

    def get_success_url(self):
        return reverse('church-membership-list', kwargs={'slug': self.church.slug})


class ChurchMembershipListView(ChurchAdminMembershipMixin, ListView):
    pass


class ChurchMembershipCreateView(ChurchAdminMembershipMixin, CreateView):
    form_class = ChurchMembershipForm
    permission = 1

    def form_valid(self, form):
        form.instance.church = self.church
        return super(ChurchMembershipCreateView, self).form_valid(form)


class ChurchMembershipUpdateView(ChurchAdminMembershipMixin, UpdateView):
    fields = ['title', 'permission']
    template_name = "churches/membership_update.html"
    permission = 1


class ChurchMembershipDeleteView(ChurchAdminMembershipMixin, DeleteView):
    template_name = "churches/membership_delete.html"
    permission = 1


class ChurchBlacklistView(ChurchAdminMixin, ListView):
    model = Product
    template_name = "churches/blacklist_list.html"

    def get_queryset(self):
        return super(ChurchBlacklistView, self).get_queryset().filter(church=self.church)


@login_required
def ChurchBlacklistSearchView(request, slug):
    church = get_object_or_404(
        Church,
        slug=slug,
        memberships__user=request.user,
        memberships__permission__lte=2
    )
    queryset = Product.objects.exclude(church=church).filter(
        name__icontains=request.GET.get('term', '')).values("name", "pk")
    for product in queryset:
        product['label'] = product.pop('name')
        product['value'] = product.pop('pk')
    return JsonResponse(list(queryset), safe=False)
