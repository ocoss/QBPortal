from django.conf.urls import url

from client_portal.views import FrontPageView, OrdersView, ReportsView, SettingsView, NewAccountView

urlpatterns = [
    url(r'^$', FrontPageView.as_view(), name='front_page'),
    url(r'^orders/$', OrdersView.as_view(), name='orders'),
    url(r'^reports/$', ReportsView.as_view(), name='reports'),
    url(r'^settings/$', SettingsView.as_view(), name='settings'),
    url(r'^create_account/$', NewAccountView.as_view(), name='create_account'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', 
        kwargs={'next_page':'/'}),
]
