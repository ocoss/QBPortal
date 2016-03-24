from django.db import models
from django.contrib.auth.models import User
from staff_portal.models import StaffMember


class Profile(models.Model):
    STATE_ABREVIATIONS = (
        ('SC', 'SC'),
        ('NC', 'NC'),
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
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, choices=STATE_ABREVIATIONS)
    zip_code = models.CharField(max_length = 15)

    phone_number = models.CharField(max_length=20)

    rep = models.ForeignKey(StaffMember, verbose_name="323 Sports Representative",
                               on_delete=models.SET_NULL, null=True)

    def __unicode__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
    
    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
        
    class Meta():
        ordering = ['user__last_name', 'user__first_name']
