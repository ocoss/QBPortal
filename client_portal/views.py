from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from quickbooks import QuickBooks
from quickbooks.objects.customer import Customer



class OrdersView(generic.TemplateView):
    template_name = 'client_portal/orders.html'
    
    def get_context_data(self, **kwargs):
        context = super(OrdersView, self).get_context_data(**kwargs)

        # setup API conection
        QB = settings.QUICKBOOKS
        quickbooks = QuickBooks(sandbox=True,
                                consumer_key=QB['CLIENT_KEY'],
                                consumer_secret=QB['CLIENT_SECRET'],
                                access_token=QB['ACCESS_TOKEN'],
                                access_token_secret=QB['ACCESS_TOKEN_SECRET'],
                                company_id=QB['REALM_ID']
                                )

        # query api
        context['customers'] = Customer.all()

        return context


class ReportsView(generic.TemplateView):
    template_name = 'client_portal/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super(ReportsView, self).get_context_data(**kwargs)
        return context


class SettingsView(generic.TemplateView):
    template_name = 'client_portal/settings.html'
    
    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        return context
