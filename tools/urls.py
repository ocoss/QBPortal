from django.conf.urls import url

from tools.views import PopulateDBView

urlpatterns = [
    url(r'^$', PopulateDBView.as_view(), name='populate_db'),
]
