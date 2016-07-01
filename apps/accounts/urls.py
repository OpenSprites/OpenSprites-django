from django.conf.urls import url

from apps.accounts.views import Login, Join

urlpatterns = [
    url(r'^login/?$', Login.as_view(), name='login'),
    url(r'^join/?$', Join.as_view(), name='join'),
]
