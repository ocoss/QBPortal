from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from client_portal.models import Profile


class NewClientAccountForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['order_name',]

    email = forms.EmailField()

    def save(self):
        # generate a random login
        try:
            while True:
                username = User.objects.make_random_password(length=6)
                User.objects.get(username=username)
        except User.DoesNotExist:
            pass

        password = User.objects.make_random_password()

        print("{} - {}".format(username, password))

        # create a new, inactive user profile
        new_user = User.objects.create_user(username)
        new_user.email = self.cleaned_data['email']
        new_user.set_password(password)
        new_user.save()
        
        profile = Profile(user=new_user, activated=False,
                          order_name=self.cleaned_data['order_name'])
        profile.save()
        return profile



class ActivateAccountForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = []

    username = forms.CharField(max_length=30)
    password_1 = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password_2 = forms.CharField(max_length=30, widget=forms.PasswordInput())

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
                raise forms.ValidationError("password 2 doesn't match password 1.")

        return self.cleaned_data['password_2']

    def save(self, profile):
        # update info
        user = profile.user
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password_1'])
        user.save()

        profile.activated = True
        profile.save()

        return profile
