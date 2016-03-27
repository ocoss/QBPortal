from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin



class StaffOrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'staff_portal/staff_orders.html'
    
    def get_context_data(self, **kwargs):
        context = super(StaffOrdersView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        # redirect to client page if not staff member
        if not hasattr(request.user, 'staffmember'):
            return redirect('orders')
        return super(StaffOrdersView, self).dispatch(request, *args, **kwargs)



class StaffReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'staff_portal/staff_reports.html'
    
    def get_context_data(self, **kwargs):
        context = super(StaffReportsView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        # redirect to client page if not staff member
        if not hasattr(request.user, 'staffmember'):
            return redirect('reports')
        return super(StaffReportsView, self).dispatch(request, *args, **kwargs)



class StaffSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'staff_portal/staff_settings.html'
    
    def get_context_data(self, **kwargs):
        context = super(StaffSettingsView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        # redirect to client page if not staff member
        if not hasattr(request.user, 'staffmember'):
            return redirect('settings')
        return super(StaffSettingsView, self).dispatch(request, *args, **kwargs)
