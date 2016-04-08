from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from my_quickbooks import QuickBooks
from my_quickbooks.objects.invoice import Invoice

from client_portal.models import Profile, Order, Payment
from staff_portal.models import StaffMember



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

        # create orders from invoice info
        for invoice in invoices:
            # parse user info
            user_info = invoice.CustomerRef.split()
            # trim extra commas
            if user_info[1].endswith(','):
                user_info[1] = user_info[1][:-1]
            if user_info[2].endswith(','):
                user_info[2] = user_info[2][:-1]
            
            # try to find associated user profile
            try:
                profile = Profile.objects.get(user__first_name=user_info[0], user__last_name=user_info[1], city=user_info[2], state=user_info[3])

            # user does not have an online profile
            except ObjectDoesNotExist:
                continue

            # try to find associated rep
            for cf in invoice.CustomField:
                if cf.Name == "SALES REP":
                    rep_code = cf.StringValue
                    try:
                        rep = StaffMember.objects.get(qb_code=rep_code)
                    except ObjectDoesNotExist
                        rep = None
                    break
            else:
                rep = None
            

            order = Order(client=profile, rep=rep)




        # convert to custom django models
        context['data'] = invoices[0]

        return context

    def dispatch(self, request, *args, **kwargs):
        # redirect to staff page if staff member
        if not request.user.is_superuser:
            return redirect('orders')
        return super(PopulateDBView, self).dispatch(request, *args, **kwargs)
