from django.conf.urls import url, include

from .views import church as views

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/', include([
        url(r'^$', views.ChurchHomeView.as_view(), name='church-home'),
        # url(r'^login/$', views.ChurchLoginView.as_view(), name='church-login'),
        # url(r'^admin/$', views.ChurchAdminListView.as_view(),
        #     name='church-admin-list'),
    ])),
]
