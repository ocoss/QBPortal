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
        invoices = Invoice.all(max_results=1000)

        # create orders from invoice info
        for invoice in invoices:
            # parse user info
            # should be {name/org}, {city}, {state (2 letter)}
            # but some are missing second comma :(
            user_info = invoice.CustomerRef.name.split(',')

            # handle missing comma case
            if len(user_info) == 2
                city_state = user_info[1].strip()
                user_info[1] = city_state[:-3].strip()
                user_info.append(city_state[-2:])

            # try to find associated user profile
            name = user_info[0].split()
            
            if len(name) == 2:
                # could be person's name
                try:
                    profile = Profile.objects.get(user__first_name=name[0].strip(), user__last_name=name[1].strip(), city=user_info[1].strip(), state=user_info[2].strip())

                # user does not have an online profile
                except ObjectDoesNotExist:
                    pass

            # could be org name
            try:
                profile = Profile.objects.get(org_name=user_info[0].strip(), city=user_info[1].strip(), state=user_info[2].strip())

            # org does not have an online profile
            except ObjectDoesNotExist:
                profile = None

            # try to find associated rep
            for cf in invoice.CustomField:
                if cf.Name == "SALES REP":
                    rep_code = cf.StringValue.strip()
                    try:
                        rep = StaffMember.objects.get(qb_code=rep_code)
                    except ObjectDoesNotExist
                        rep = None
                    break
            else:
                rep = None
            

            # convert to custom django model
            order = Order(client=profile, rep=rep)









        return context

    def dispatch(self, request, *args, **kwargs):
        # redirect to staff page if staff member
        if not request.user.is_superuser:
            return redirect('orders')
        return super(PopulateDBView, self).dispatch(request, *args, **kwargs)
