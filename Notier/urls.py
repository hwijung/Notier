from django.conf.urls import patterns, include, url
from django.contrib import admin
from alarm.views import *
import os.path

admin.autodiscover()

contents = os.path.join (
    os.path.dirname( __file__ ), 'contents' )

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', main),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^beat/', beat), 
    
    # Media
    url(r'^contents/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': contents }),
)
 