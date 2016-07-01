from django.conf.urls import url

from apps.accounts.views import Login, Join, AccountPage

urlpatterns = [
    url(r'^login/?$', Login.as_view(), name='login'),
    url(r'^join/?$', Join.as_view(), name='join'),
    url(r'^you/?$', AccountPage.as_view(), {'user':''}, name='account'),
    url(r'^users/(?P<user>[a-zA-Z0-9-]+)', AccountPage.as_view(), name='account'),
]
