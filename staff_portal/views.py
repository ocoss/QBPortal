from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from staff_portal.forms import NewStaffAccountForm
from client_portal.forms import NewClientAccountForm
from client_portal.models import Profile



class StaffBaseView(LoginRequiredMixin, TemplateView):
    client_redirect = 'front_page'

    def dispatch(self, request, *args, **kwargs):
        # redirect to client page if not a staff member
        if not hasattr(request.user, 'staffmember'):
            return redirect(self.client_redirect)
        return super(StaffBaseView, self).dispatch(request, *args, **kwargs)



class StaffOrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'staff_portal/staff_orders.html'
    client_redirect = 'orders'
    
    def get_context_data(self, **kwargs):
        context = super(StaffOrdersView, self).get_context_data(**kwargs)
        return context



class StaffReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'staff_portal/staff_reports.html'
    client_redirect = 'reports'
    
    def get_context_data(self, **kwargs):
        context = super(StaffReportsView, self).get_context_data(**kwargs)
        return context



class StaffSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'staff_portal/staff_settings.html'
    client_redirect = 'settings'
    
    def get_context_data(self, **kwargs):
        context = super(StaffSettingsView, self).get_context_data(**kwargs)
        context['clients'] = Profile.objects.all()
        return context



# class StaffCreateAccountView(LoginRequiredMixin, TemplateView):
#     template_name = 'staff_portal/staff_create_account.html'
#     client_redirect = 'settings'

#     def get_context_data(self, **kwargs):
#         context = super(StaffCreateAccountView, self).get_context_data(**kwargs)
#         context['form'] = NewClientAccountForm()
#         return context

#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         form = NewClientAccountForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('staff_settings')
#         context['form'] = form
#         return render(request, self.template_name, context)



class CreateStaffView(LoginRequiredMixin, TemplateView):
    template_name = 'staff_portal/create_staff.html'
    client_redirect = 'settings'

    def get_context_data(self, **kwargs):
        context = super(CreateStaffView, self).get_context_data(**kwargs)
        context['form'] = NewStaffAccountForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = NewStaffAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_settings')
        context['form'] = form
        return render(request, self.template_name, context)

    def dispatch(self, request, *args, **kwargs):
        # make sure user is a superuser
        if not request.user.is_superuser:
            return redirect('staff_settings')
        return super(CreateStaffView, self).dispatch(request, *args, **kwargs)
