from django.db import models
from django.contrib.auth.models import User


class StaffMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
    
    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
        
    class Meta():
        ordering = ['user__last_name', 'user__first_name']
