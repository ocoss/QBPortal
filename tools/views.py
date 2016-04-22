from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from my_quickbooks import QuickBooks
from my_quickbooks.objects.invoice import Invoice
from my_quickbooks.objects.customer import Customer

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


        # Customers-------------------------------------------------------------
        count = 1
        while True:
            # grab all the customers in chunks of 1000 (largest size allowed)
            customers = Customer.filter(start_position=count, max_results=1000)
            
            # update position
            count += len(customers)
            if len(customers) == 0:
                break

            # iterate through accounts
            for customer in customers:
                # make sure the account has all the neccessary info
                if not customer.PrimaryEmailAddr or not customer.DisplayName:
                    continue

                # make an account for every email address listed
                for email in str(customer.PrimaryEmailAddr).split(','):
                    email = email.strip()

                    # make sure email exists
                    if not email:
                        continue

                    # make sure the email is unique
                    if Profile.objects.filter(user__email=email).exists():
                        continue

                    # create a new profile
                    try:
                        # genereate a unique random username
                        while True:
                            username = User.objects.make_random_password(length=6)
                            User.objects.get(username=username)
                    except User.DoesNotExist:
                        pass

                    # generate a random password
                    password = User.objects.make_random_password()

                    # create a new, inactive user profile
                    new_user = User.objects.create_user(username)
                    new_user.email = email
                    new_user.set_password(password)
                    new_user.save()
                    
                    profile = Profile(user=new_user, activated=False,
                                      email_pref=True,
                                      display_name=customer.DisplayName)
                    profile.save()


        # Invoices--------------------------------------------------------------

        count = 1
        while True:
            # get all invoices in chunks of 1000 (largesst size allowed)
            invoices = Invoice.all(start_position=count, max_results=2)

            # update position
            count += len(invoices)
            if len(invoices) == 0:
                break

            # create orders from invoice info
            for invoice in invoices:

                # get associated rep code
                rep_code = ''
                for cf in invoice.CustomField:
                    if cf.Name == "SALES REP":
                        rep_code = cf.StringValue.strip()

                items = ''
                for line in invoice.Line:
                    items += line

                order = Order(id_num=invoice.ID, rep_code=rep_code, 
                              date=invoice.DueDate, is_estimate=False,
                              is_invoice=True, items=items,
                              total_amount=invoice.TotalAmt,
                              total_owed=invoice.TotalAmt)
                order.save()

                # These are all the id's of the estimates
                # for l in invoice.LinkedTxn:
                #     l

                # get associated email addresses
                emails = str(invoice.BillEmail).split(',')
                for email in emails:
                    email = email.strip()
                    try:
                        profile = User.objects.get(email=email).profile
                        order.client.add(profile)
                    except ObjectDoesNotExist:
                        pass
            
            break


        return context

    def dispatch(self, request, *args, **kwargs):
        # redirect to staff page if staff member
        if not request.user.is_superuser:
            return redirect('orders')
        return super(PopulateDBView, self).dispatch(request, *args, **kwargs)
