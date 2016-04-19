from django.conf.urls import url

from staff_portal.views import StaffOrdersView, StaffReportsView, StaffSettingsView, \
                               CreateStaffView # ,StaffCreateAccountView

urlpatterns = [
    url(r'^orders/$', StaffOrdersView.as_view(), name='staff_orders'),
    url(r'^reports/$', StaffReportsView.as_view(), name='staff_reports'),
    url(r'^settings/$', StaffSettingsView.as_view(), name='staff_settings'),
    # url(r'^settings/create_account/$', StaffCreateAccountView.as_view(), name='staff_create_account'),
    url(r'^create_staff/$', CreateStaffView.as_view(), name='create_staff'),
]
