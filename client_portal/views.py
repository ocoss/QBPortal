from django.conf import settings
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from quickbooks import QuickBooks
from quickbooks.objects.customer import Customer



class OrdersView(generic.TemplateView):
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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # redirect to staff page if staff member
        if hasattr(request.user, 'staffmember'):
            return redirect('staff_orders')
        return super(OrdersView, self).dispatch(request, *args, **kwargs)



class ReportsView(generic.TemplateView):
    template_name = 'client_portal/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super(ReportsView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # redirect to staff page if staff member
        if hasattr(request.user, 'staffmember'):
            return redirect('staff_reports')
        return super(ReportsView, self).dispatch(request, *args, **kwargs)



class SettingsView(generic.TemplateView):
    template_name = 'client_portal/settings.html'
    
    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # redirect to staff page if staff member
        if hasattr(request.user, 'staffmember'):
            return redirect('staff_settings')
        return super(SettingsView, self).dispatch(request, *args, **kwargs)
