from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import logout
from subprocess import Popen
import json 

from alarm.forms import *
from alarm.models import *

# celery beat flag and process
beat = 0
beat_process = 0

# Create your views here.
def main (request):
    return render_to_response ( 'index.html' )

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
   
     