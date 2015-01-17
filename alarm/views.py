from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from subprocess import Popen
import json 
 
from alarm.forms import *
from alarm.models import *

import logging, logging.config
import sys

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
     
    entries = user.monitoringentry_set.order_by ( 'title' )
    number_of_entries = len(entries)
    settings = UserSettings.objects.get(user=user)
    
    variables = RequestContext( request, { 'username': username, 'noe': number_of_entries, 'entries': entries, 'beat': settings.beat } )
    return render_to_response( 'user_page.html', variables ) 

def setting_page(request, username):
    user = get_object_or_404 ( User, username = username )
    settings = UserSettings.objects.get(user=user)
    
    variables = RequestContext( request, { 'username': username, 'settings': settings } )
    return render_to_response( 'setting_page.html', variables ) 
    
def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        logging.info(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            
            logging.info( "" + username + password + email )
            
            if username:
                user = User.objects.create_superuser(username, email, password)
                user_setting = UserSettings.objects.create(beat=True, user = user)
                user_setting.save()
                return HttpResponseRedirect('/register/success')
            else:
                return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
        
    variables = RequestContext( request, {'form': form} )
    return render_to_response( 'registration/register.html', variables )

def login_page( request ):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            return render_to_response('login.html', { 'error': True } , context_instance=RequestContext(request))    
    return render_to_response('login.html', context_instance=RequestContext(request))    
    
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
    
    variables = RequestContext( request, { 'username': request.user.username, 'form': form })
    
    return render_to_response( 'entry_save.html', variables )

def _entry_save( request, form ):
    # Create or get Site
    site, dummy = Site.objects.get_or_create( url = form.cleaned_data['url'])
    
    # Create or get Keyword
    keyword, dummy = Keyword.objects.get_or_create( text = form.cleaned_data['keyword'])
    
    title = form.cleaned_data['title']
    
    # Create or get Entry
    entry, created = MonitoringEntry.objects.get_or_create( user = request.user, 
                                                            site = site, 
                                                            keyword = keyword,
                                                            title = title)
    
    # Save entry to database
    entry.save()
    return entry

def _entry_delete( selected_title ):
    # Delete Entry
    MonitoringEntry.objects.filter( title = selected_title ).delete()
    

@login_required
def entry_edit_page( request, selected_title ):
    if request.method == 'POST':
        form = EntryEditForm ( request.POST )
        if form.is_valid():
            _entry_update(request, form)
            return HttpResponseRedirect ( '/user/%s/' % request.user.username ) 
    elif request.GET.has_key('url'):
        url = request.GET['url']
    elif request.method == 'DELETE':
        _entry_delete( selected_title )
        obj = { "result": "success" }   
        return HttpResponse( json.dumps(obj) )   
      
    else:
        entry = MonitoringEntry.objects.get(title = selected_title)
        form = EntryEditForm(initial= {'title': entry.title, 
                                       'url': entry.site.url,
                                       'keyword': entry.keyword.text })
        
    variables = RequestContext( request, { 'username': request.user.username, 'form': form })
    return render_to_response ( 'entry_edit.html', variables )

def _entry_update( request, form ):
    # update or create Site
    site, created = Site.objects.update_or_create( url = form.cleaned_data['url'] )
    
    # Update or get Keyword
    keyword, created = Keyword.objects.update_or_create( text = form.cleaned_data['keyword'])
    
    title_from_form = form.cleaned_data['title']
    
    # Create or get Entry
    entry = MonitoringEntry.objects.get(title = title_from_form)
    entry.site = site
    entry.keyword = keyword
    
    # Save entry to database
    entry.save()
    return entry

def entry_activate( request ):  
    if request.method == 'POST':
        entry_name = request.POST.get('entry_name');
        on_or_off = request.POST.get('activate');
        obj = { "result": "success" }
 
        if request.user.is_authenticated():
            user = request.user
            entry = MonitoringEntry.objects.get(title = entry_name, user = user)
            
            if on_or_off == "ON":
                entry.activated = True
            else:
                entry.activated = False
                
            entry.save()
        
            obj = { "result": "success" }
        else:
            obj = { "result": "fail" }
       
        return HttpResponse( json.dumps(obj))
   
@login_required 
def beat(request): 
    if request.method == 'POST':
        # Turn on or off?
        on_or_off = request.POST.get('direction') 
        
         # Get User object from session
        if request.user.is_authenticated():
            user = request.user 
            settings = UserSettings.objects.get(user=user)
            if on_or_off == "ON":
                settings.beat = 1
            else:
                settings.beat = 0
                  
            settings.save()
                   
            obj = { "result": "success" }   
        else:
            obj = { "result": "fail" }   
            
        return HttpResponse( json.dumps(obj) )     
         
        '''
         global beat, beat_process
         
        if start == 'start':
            logging.info( CELERYBEAT_SCHEDULE.get('add-every-second').get('args') ) 
            # set arguments TODO : 
            CELERYBEAT_SCHEDULE.get('add-every-second')['args'] = ['http://www.naver.com']
            
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
   '''
     