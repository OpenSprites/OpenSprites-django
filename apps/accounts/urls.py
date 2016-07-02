from django.conf.urls import url

from apps.accounts.views import Login, Join, AccountPage, Logoff

urlpatterns = [
    url(r'^login/?$', Login.as_view(), name='login'),
    url(r'^signout/?$', Logoff.as_view(), name='logoff'),
    url(r'^join/?$', Join.as_view(), name='join'),
    url(r'^you/?$', AccountPage.as_view(), name='you'),
    url(r'^users/(?P<user>[a-zA-Z0-9-]+)', AccountPage.as_view(), name='account'),
]
