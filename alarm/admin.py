from django.contrib import admin
from alarm.models import *

admin.site.register(Site)
admin.site.register(Keyword)
admin.site.register(MonitoringEntry)
