from django.conf.urls import url

from apps.accounts.views import ResourceUploadView

urlpatterns = [
    url(r'^share/?$', ResourceUploadView.as_view(), name='share'),
]
