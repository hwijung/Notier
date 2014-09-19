from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from subprocess import Popen
import json 

# celery beat flag and process
beat = 0
beat_process = 0

# Create your views here.
def main (request):
    return render_to_response ( 'index.html' )

def beat(request): 
    if request.method == 'POST':
        start = request.POST['start']
        global beat, beat_process
        
        if start:
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
   
     