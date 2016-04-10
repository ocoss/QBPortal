from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from client_portal.models import Profile


class NewAccountForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['organization', 'billing_address', 'city', 'state', 'zip_code',
                  'phone_number',]

    username   = forms.CharField(max_length=30)
    password_1 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password_2 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    first_name = forms.CharField()
    last_name  = forms.CharField()
    email      = forms.EmailField()

    def clean_username(self):
        # Check if username exists
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']

        raise forms.ValidationError("Username is already in use.")

    def clean_password_1(self):
        # make sure password is valid
        if 'password_1' in self.cleaned_data:
            validate_password(self.cleaned_data['password_1'])

        return self.cleaned_data['password_1']

    def clean_password_2(self):
        # check if password_1 and password_2 match each other
        if 'password_1' in self.cleaned_data and 'password_2' in self.cleaned_data:
            if self.cleaned_data['password_1'] != self.cleaned_data['password_2']:
                raise forms.ValidationError("password_2 doesn't match password_1.")

        return self.cleaned_data['password_2']

    def save(self):
        # create new user
        new_user = User.objects.create_user(self.cleaned_data['username'],
                                            self.cleaned_data['email'],
                                            self.cleaned_data['password_1'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()
        profile = Profile(user=new_user,
                          organization=self.cleaned_data['organization'],
                          billing_address=self.cleaned_data['billing_address'],
                          city=self.cleaned_data['city'],
                          state=self.cleaned_data['state'],
                          zip_code=self.cleaned_data['zip_code'],
                          phone_number=self.cleaned_data['phone_number'])
        profile.save()
        return profile



class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['organization', 'billing_address', 'city', 'state',
                  'zip_code', 'phone_number', 'email_verified', 'rep_verified',]

    def save(self, pk):
        profile = get_object_or_404(Profile, pk=pk)
        # get all the new invoices if newly approved
        if not profile.rep_verified and self.cleaned_data['rep_verified']:
            pass
            # pull new stuff here

        # update info
        profile.organization = self.cleaned_data['organization']
        profile.billing_address = self.cleaned_data['billing_address']
        profile.city = self.cleaned_data['city']
        profile.state = self.cleaned_data['state']
        profile.zip_code = self.cleaned_data['zip_code']
        profile.email_verified = self.cleaned_data['email_verified']
        profile.rep_verified = self.cleaned_data['rep_verified']

        profile.save()
        return profile
