from django.conf.urls import url

from client_portal.views import FrontPageView, OrdersView, ReportsView, SettingsView, \
                                ActivateAccountView

urlpatterns = [
    url(r'^$', FrontPageView.as_view(), name='front_page'),
    url(r'^orders/$', OrdersView.as_view(), name='orders'),
    url(r'^reports/$', ReportsView.as_view(), name='reports'),
    url(r'^settings/$', SettingsView.as_view(), name='settings'),
    url(r'^activate_account/$', ActivateAccountView.as_view(), name='activate_account'),
]
