from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from staff_portal.models import StaffMember
from client_portal.models import Profile


class NewStaffForm(forms.ModelForm):
    class Meta:
        model = StaffMember
        fields = []

    username = forms.CharField(max_length=30)
    password_1 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password_2 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

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
        
        staff = StaffMember(user=new_user)
        staff.save()
        return staff
