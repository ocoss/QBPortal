from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from staff_portal.forms import NewStaffForm
from client_portal.forms import UpdateAccountForm
from client_portal.models import Profile



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
        context['clients'] = Profile.objects.all()
        return context

    def dispatch(self, request, *args, **kwargs):
        # redirect to client page if not staff member
        if not hasattr(request.user, 'staffmember'):
            return redirect('settings')
        return super(StaffSettingsView, self).dispatch(request, *args, **kwargs)



class StaffUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'staff_portal/staff_update_account.html'

    def get_context_data(self, **kwargs):
        context = super(StaffUpdateView, self).get_context_data(**kwargs)
        client_pk = self.kwargs['pk']
        context['pk'] = client_pk
        profile = get_object_or_404(Profile, pk=client_pk)
        context['client'] = profile
        context['form'] = UpdateAccountForm(instance=profile)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = UpdateAccountForm(request.POST)
        if form.is_valid():
            form.save(kwargs['pk'])
            return redirect('staff_settings')
        context['form'] = form
        return render(request, self.template_name, context)

    def dispatch(self, request, *args, **kwargs):
        # redirect to client page if not staff member
        if not hasattr(request.user, 'staffmember'):
            return redirect('settings')
        return super(StaffUpdateView, self).dispatch(request, *args, **kwargs)



class CreateStaffView(LoginRequiredMixin, TemplateView):
    template_name = 'staff_portal/create_staff.html'

    def get_context_data(self, **kwargs):
        context = super(CreateStaffView, self).get_context_data(**kwargs)
        context['form'] = NewStaffForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = NewStaffForm(request.POST)
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
