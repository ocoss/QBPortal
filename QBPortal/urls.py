from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout', kwargs={'next_page':'/'}),

    url(r'^change_password/$', auth_views.password_change, name='change_password'),
    url(r'^change_password/done/$', auth_views.password_change_done, name='password_change_done'),

    # url(r'^password_reset/$', auth_views.password_reset, name='reset_password'),
    # url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^password_reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'', include('client_portal.urls')),
    url(r'staff/', include('staff_portal.urls')),
    # url(r'tools/', include('tools.urls')),
    
    url(r'^admin/', admin.site.urls),
]
