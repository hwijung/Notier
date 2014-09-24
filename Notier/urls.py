from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

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
     
    # Session Management
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page ),
    url(r'^register/$', register_page ),
    url(r'^register/success/$', TemplateView.as_view(
            template_name='registration/register_success.html'),
              name="home" ), 
                            
    # Media
    url(r'^contents/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': contents }),
                       
    # Administration
    url(r'^admin/', include(admin.site.urls)),                       
)
 