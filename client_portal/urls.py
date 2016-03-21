from django.conf.urls import url

from client_portal.views import OrdersView, ReportsView, SettingsView

urlpatterns = [
    url(r'^$', OrdersView.as_view(), name='orders'),
    url(r'^reports/$', ReportsView.as_view(), name='reports'),
    url(r'^settings/$', SettingsView.as_view(), name='settings'),
]
