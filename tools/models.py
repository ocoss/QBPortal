from django.db import models
from staff_portal.models import StaffMember
from client_portal.models import Profile



class Order(models.Model):
    # people associated with this order
    client = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rep = models.ForeignKey(StaffMember, verbose_name="323 Sports Representative",
                               on_delete=models.SET_NULL, null=True)

    # when the order/estimate was created
    date = models.DateField()

    # to determine if payments can be made
    is_estimate = models.BooleanField(default=True)
    is_invoiced = models.BooleanField(default=False)

    # need to figure out how to store this
    items = models.CharField(max_length=100)

    # the total cost of the order
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    # total_owed = total_amount - payments
    total_owed = models.DecimalField(max_digits=8, decimal_places=2)
    # if total_owed is zero
    payed_off = models.BooleanField(default=False)
    

    class Meta():
        ordering = ['date']

    # def __unicode__(self):
    #     return ""
    
    # def __str__(self):
    #     return ""



class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()

    class Meta():
        ordering = ['date']
