from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^tools$', views.index, name='tools_index'),
]
