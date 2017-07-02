from django.conf.urls import url, include

from .views import dashboard as views

urlpatterns = [
    url(r'^$', views.ChurchListView.as_view(), name='church-list'),
    url(r'^add/$', views.ChurchCreateView.as_view(), name='church-add'),
    url(r'^(?P<pk>[0-9]+)/', include([
        url(r'^$', views.ChurchDetailView.as_view(), name='church-detail'),
        url(r'^members/add/$', views.ChurchMembershipCreateView.as_view(),
            name='church-membership-create'),
    ])),
]
