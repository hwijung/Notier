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
    url(r'^bootstrap/', TemplateView.as_view(
            template_name='bootstrap.html'), name="home" ), 

    url(r'^$', main),
    url(r'^user/(\w+)/$', user_page ),
    url(r'^settings/(\w+)/$', setting_page ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^beat/', beat), 
     
    # Session Management
    url(r'^login/$', login_page),
    url(r'^logout/$', logout_page ),
    url(r'^register/$', register_page ),
    url(r'^register/success/$', TemplateView.as_view(
            template_name='registration/register_success.html'),
              name="home" ), 
                        
    # Account Management                   
    url(r'^entry/save/$', entry_save_page),
    url(r'^entry/activate/$', entry_activate),
    url(r'^entry/(\w+)/$', entry_edit_page),
    url(r'^entry/$', entry_edit_page),         
                             
    # Media
    url(r'^contents/(?P<path>.*)$', 'django.views.static.serve', 
        { 'document_root': contents }),
                       
    # Administration
    url(r'^admin/', include(admin.site.urls)),                       
)
 