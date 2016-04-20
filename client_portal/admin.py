from django.contrib import admin
from client_portal.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'get_email', 'activated', 'email_pref',]

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"

admin.site.register(Profile, ProfileAdmin)
