from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps.core.views import Index

urlpatterns = patterns('',

	# Index views
    url(r'^$', Index.as_view(), name='index'),
    url(r'^', include('apps.accounts.urls')),
    url(r'^', include('apps.resources.urls')),

    url(r'^(?i)admin/?', include(admin.site.urls)),
)
