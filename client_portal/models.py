from django.db import models
from django.contrib.auth.models import User
from staff_portal.models import StaffMember



class Profile(models.Model):
    STATE_ABREVIATIONS = (
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
)

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
    # (* optional; Make required in forms)
    
    # additional info goes here
    organization = models.CharField(max_length=200)
    billing_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, choices=STATE_ABREVIATIONS)
    zip_code = models.CharField(max_length = 15)

    phone_number = models.CharField(max_length=20)

    email_verified = models.BooleanField(default=False)
    rep_verified = models.BooleanField(default=False)
    
    class Meta():
        ordering = ['user__last_name', 'user__first_name']

    def __unicode__(self):
        return "{} {}: {}".format(self.user.first_name, self.user.last_name,
                                  self.organization)
    
    def __str__(self):
        return "{} {}: {}".format(self.user.first_name, self.user.last_name,
                                  self.organization)



class Order(models.Model):
    # people associated with this order
    client = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rep = models.ForeignKey(StaffMember, on_delete=models.SET_NULL, null=True)

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



class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()

    class Meta():
        ordering = ['date']
