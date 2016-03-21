from django.conf.urls import url

from staff_portal.views import StaffOrdersView, StaffReportsView

urlpatterns = [
    url(r'^$', StaffOrdersView.as_view(), name='orders'),
    url(r'^reports/$', StaffReportsView.as_view(), name='reports'),
]
