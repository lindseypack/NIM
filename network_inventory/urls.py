from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'network_inventory.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^devices/', include('devices.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
