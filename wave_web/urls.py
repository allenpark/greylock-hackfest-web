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
    url(r'^$', index)
)

urlpatterns += staticfiles_urlpatterns()
