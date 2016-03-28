from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from client_portal.forms import NewAccountForm

from quickbooks import QuickBooks
from quickbooks.objects.customer import Customer



class OrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'client_portal/orders.html'
    
    def get_context_data(self, **kwargs):
        context = super(OrdersView, self).get_context_data(**kwargs)

        # setup API conection
        # QB = settings.QUICKBOOKS
        # quickbooks = QuickBooks(sandbox=True,
        #                         consumer_key=QB['CLIENT_KEY'],
        #                         consumer_secret=QB['CLIENT_SECRET'],
        #                         access_token=QB['ACCESS_TOKEN'],
        #                         access_token_secret=QB['ACCESS_TOKEN_SECRET'],
        #                         company_id=QB['REALM_ID']
        #                         )

        # # query api
        # context['customers'] = Customer.all()

        return context

    def dispatch(self, request, *args, **kwargs):
        # redirect to staff page if staff member
        if hasattr(request.user, 'staffmember'):
            return redirect('staff_orders')
        return super(OrdersView, self).dispatch(request, *args, **kwargs)



class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'client_portal/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super(ReportsView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        # redirect to staff page if staff member
        if hasattr(request.user, 'staffmember'):
            return redirect('staff_reports')
        return super(ReportsView, self).dispatch(request, *args, **kwargs)



class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'client_portal/settings.html'
    
    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        # redirect to staff page if staff member
        if hasattr(request.user, 'staffmember'):
            return redirect('staff_settings')
        return super(SettingsView, self).dispatch(request, *args, **kwargs)



class NewAccountView(TemplateView):
    template_name = 'client_portal/create_account.html'

    def get_context_data(self, **kwargs):
        context = super(NewAccountView, self).get_context_data(**kwargs)
        context['form'] = NewAccountForm()
        return context

    def dispatch(self, request, *args, **kwargs):
        # check if already logged in
        if request.user.is_authenticated():
            return redirect('orders')
        return super(NewAccountView, self).dispatch(request, *args, **kwargs)
