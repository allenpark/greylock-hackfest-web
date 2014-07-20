from django.conf.urls import patterns, include, url
from wave_web.views import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wave_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/$', wave_admin),
    url(r'^$', index),
    url(r'^settings/$', settings),
    url(r'^api/getNumUsersOnChannelInRadius/(?P<channel>\w+)/(?P<latitude>[-]?[\d.]+)/(?P<longitude>[-]?[\d.]+)/(?P<radius>[\d.]+)$', get_num_users_in_radius)
)

urlpatterns += staticfiles_urlpatterns()

(r'^search/(?P<query>\w+)$', 'twingle.search.views.index'),
