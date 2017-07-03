from django.conf.urls import url, include

from .views import church as views

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/', include([
        url(r'^$', views.ChurchHomeView.as_view(), name='church-home'),
        url(r'^members/$', views.ChurchMembershipListView.as_view(),
            name='church-membership-list'),
        url(r'^members/add/$', views.ChurchMembershipCreateView.as_view(),
            name='church-membership-create'),
        url(r'^members/(?P<pk>[0-9]+)/$', views.ChurchMembershipUpdateView.as_view(),
            name='church-membership-update'),
    ])),
]
