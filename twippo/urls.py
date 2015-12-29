from django.conf.urls import patterns, include, url
from django.contrib import admin

from twippo import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^track-updated/', views.track_updated, name='track_updated'),
)
