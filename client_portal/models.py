from django.db import models
from django.contrib.auth.models import User

from staff_portal.models import StaffMember



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user has the following fields:
    # - username
    # - first_name*
    # - last_name*
    # - email*
    # - password
    # - groups
    # - user_permission
    # - is_staff
    # - is_active
    # - is_superuser
    # - last_login
    # - date_joined
    # (* = optional)

    # additional info goes here
    display_name = models.CharField(max_length=200)
    activated = models.BooleanField(default=False)


    class Meta():
        ordering = ['user__email', 'display_name',]

    def __unicode__(self):
        return self.display_name

    def __str__(self):
        return self.display_name



class Order(models.Model):
    # people associated with this order
    client = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rep = models.ForeignKey(StaffMember, on_delete=models.SET_NULL, null=True,
                            blank=True)

    # when the order/estimate was created
    date = models.DateField()

    # to determine if payments can be made
    is_estimate = models.BooleanField(default=True)
    is_invoiced = models.BooleanField(default=False)

    # need to figure out how to store this
    items = models.CharField(max_length=1000)

    # the total cost of the order
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    # total_owed = total_amount - payments
    total_owed = models.DecimalField(max_digits=8, decimal_places=2)
    # if total_owed is zero
    payed_off = models.BooleanField(default=False)


    class Meta():
        ordering = ['date']



class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()


    class Meta():
        ordering = ['order', 'date']
