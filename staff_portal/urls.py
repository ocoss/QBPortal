from django.conf.urls import url

from staff_portal.views import StaffOrdersView, StaffReportsView, StaffSettingsView, CreateStaffView

urlpatterns = [
    url(r'^orders/$', StaffOrdersView.as_view(), name='staff_orders'),
    url(r'^reports/$', StaffReportsView.as_view(), name='staff_reports'),
    url(r'^settings/$', StaffSettingsView.as_view(), name='staff_settings'),
    url(r'^create_staff/$', CreateStaffView.as_view(), name='create_staff'),
]
