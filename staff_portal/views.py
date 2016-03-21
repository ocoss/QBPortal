from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse



class StaffOrdersView(generic.TemplateView):
    template_name = 'staff_portal/staff_orders.html'
    
    def get_context_data(self, **kwargs):
        context = super(StaffOrdersView, self).get_context_data(**kwargs)
        return context


class StaffReportsView(generic.TemplateView):
    template_name = 'staff_portal/staff_reports.html'
    
    def get_context_data(self, **kwargs):
        context = super(StaffReportsView, self).get_context_data(**kwargs)
        return context

