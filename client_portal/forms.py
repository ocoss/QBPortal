from django import forms
from client_portal.models import Profile


class NewAccountForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['street_address', 'city', 'state', 'zip_code', 'phone_number',
                  'rep', ]

    username = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    first_name = forms.CharField()
    last_name = forms.CharField()
    email=forms.EmailField()
