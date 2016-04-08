from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from quickbooks import QuickBooks
from quickbooks.objects.customer import Customer

from tools.models import Order, Payment
from client_portal import Profile
from staff_portal import Representative


class PopulateDBView(LoginRequiredMixin, TemplateView):
    template_name = 'tools/populate_db.html'
    
    def get_context_data(self, **kwargs):
        context = super(PopulateDBView, self).get_context_data(**kwargs)
        # setup API conection
        QB = settings.QUICKBOOKS
        quickbooks = QuickBooks(sandbox=False,
                                consumer_key=QB['CLIENT_KEY'],
                                consumer_secret=QB['CLIENT_SECRET'],
                                access_token=QB['ACCESS_TOKEN'],
                                access_token_secret=QB['ACCESS_TOKEN_SECRET'],
                                company_id=QB['REALM_ID']
                                )

        # get all info from api in lists of objects
        invoices = Invoice.all(max_results=10)

        # convert to custom django models


        return context

    def dispatch(self, request, *args, **kwargs):
        # redirect to staff page if staff member
        if not request.user.is_superuser
            return redirect('orders')
        return super(PopulateDBView, self).dispatch(request, *args, **kwargs)
