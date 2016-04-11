from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from client_portal.models import Profile

from client_portal.forms import ActivateAccountForm



class ClientBaseView(LoginRequiredMixin, TemplateView):
    staff_redirect = 'front_page'
    
    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'staffmember'):
            return redirect(self.staff_redirect)
        if hasattr(request.user, 'profile') and not request.user.profile.activated:
            return redirect('activate_account')
        return super(ClientBaseView, self).dispatch(request, *args, **kwargs)



class FrontPageView(TemplateView):
    template_name = 'client_portal/front_page.html'



class OrdersView(ClientBaseView):
    template_name = 'client_portal/orders.html'
    staff_redirect = 'staff_orders'
    
    def get_context_data(self, **kwargs):
        context = super(OrdersView, self).get_context_data(**kwargs)
        return context



class ReportsView(ClientBaseView):
    template_name = 'client_portal/reports.html'
    staff_redirect = 'staff_reports'
    
    def get_context_data(self, **kwargs):
        context = super(ReportsView, self).get_context_data(**kwargs)
        return context



class SettingsView(ClientBaseView):
    template_name = 'client_portal/settings.html'
    staff_redirect = 'staff_settings'
    
    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        return context



class ActivateAccountView(ClientBaseView):
    template_name = 'client_portal/activate_account.html'

    def get_context_data(self, **kwargs):
        context = super(ActivateAccountView, self).get_context_data(**kwargs)
        context['form'] = ActivateAccountForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ActivateAccountForm(request.POST)
        if form.is_valid():
            form.save(request.user.profile)
            return redirect('orders')
        context['form'] = form
        return render(request, self.template_name, context)

    def dispatch(self, request, *args, **kwargs):
        # check if already active
        if request.user.profile.activated:
            return redirect('front_page')
        if hasattr(request.user, 'staffmember'):
            return redirect('front_page')
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
