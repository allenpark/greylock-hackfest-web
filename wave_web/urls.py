from django.conf.urls import patterns, include, url
from wave_web.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wave_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', wave_admin),
)
