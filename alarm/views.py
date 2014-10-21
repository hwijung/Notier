from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from subprocess import Popen
import json 
 
from alarm.forms import *
from alarm.models import *

import logging, logging.config
import sys

# celery beat flag and process
beat = 0
beat_process = 0

# Get an instance of a logger
LOGGING = { 
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)

# Create your views here.
def main (request):
    # username = request.user.username
    # user = get_object_or_404 ( User, username = username )
    # logging.info(user.__str__)   
    # variables = RequestContext( request, { 'username': username } )
    variables = RequestContext( request )
        
    return render_to_response ( 'index.html', variables )

def user_page(request, username):
    user = get_object_or_404 ( User, username = username )
    
    entries = user.monitoringentry_set.order_by ( '-id' )
    
    variables = RequestContext( request, { 'username': username, 'entries': entries  } )
    return render_to_response( 'user_page.html', variables ) 

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            
            if username:
                user = User.objects.create_user(username, email, password)
                return HttpResponseRedirect('/register/success')
            else:
                return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
        
    variables = RequestContext( request, {'form': form} )
    return render_to_response( 'registration/register.html', variables )


def logout_page ( request ):
    logout ( request )
    return HttpResponseRedirect ( '/' )

@login_required
def entry_save_page ( request ):
    ajax = request.GET.has_key ( 'ajax' )
    
    if request.method == 'POST':
        form = EntrySaveForm ( request.POST )
        if form.is_valid():
            _entry_save(request, form)
            return HttpResponseRedirect ( '/user/%s/' % request.user.username )
        
    elif request.GET.has_key('url'):
        url = request.GET['url']
    else:
        form = EntrySaveForm()
    
    variables = RequestContext( request, { 'form': form })
    
    return render_to_response( 'entry_save.html', variables )

def _entry_save( request, form ):
    # Create or get Site
    site, dummy = Site.objects.get_or_create( url = form.cleaned_data['url'])
    
    # Create or get Keyword
    keyword, dummy = Keyword.objects.get_or_create( text = form.cleaned_data['keyword'])
    
    title = form.cleaned_data['title']
    frequency = form.cleaned_data['frequency']
    
    # Create or get Entry
    entry, created = MonitoringEntry.objects.get_or_create( user = request.user, 
                                                            site = site, 
                                                            keyword = keyword,
                                                            title = title, 
                                                            frequency = frequency )
    
    # Save entry to database
    entry.save()
    return entry

def beat(request): 
    if request.method == 'POST':
        start = request.POST['start']
        global beat, beat_process
        
        if start == 'start':
            beat_process = Popen(['celery','-A','Notier','worker','-l','info','--beat'])
            # celery -A Notier worker -l info --beat
            beat = 1
            json_data = json.dumps({'result':1 })
            return HttpResponse(json_data, mimetype="application/json")
         
        else: 
            if beat_process != 0:
                beat_process.terminate()
            beat = 0
            json_data = json.dumps({'result':0 })
            return HttpResponse(json_data, mimetype="application/json")
   
     