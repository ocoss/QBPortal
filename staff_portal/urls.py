from django.conf.urls import url

from staff_portal.views import StaffOrdersView, StaffReportsView, StaffSettingsView

urlpatterns = [
    url(r'^$', StaffOrdersView.as_view(), name='staff_orders'),
    url(r'^reports/$', StaffReportsView.as_view(), name='staff_reports'),
    url(r'^settings/$', StaffSettingsView.as_view(), name='staff_settings'),
]
