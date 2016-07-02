from django.conf.urls import url

from .views import ResourceUploadView

urlpatterns = [
    url(r'^share/?$', ResourceUploadView.as_view(), name='share'),
]
