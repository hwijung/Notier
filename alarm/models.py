from django.db import models
from django.contrib.auth.models import User

class Site ( models.Model ):
    url = models.URLField ( unique = True )
    def __str__ (self):
        return self.url;
    class Admin:
        pass
    
class Keyword ( models.Model ):
    text = models.CharField ( max_length = 64 )
    def __str__ (self):
        return self.text;
    class Admin:
        pass
    
class UserSetting ( models.Model ):
    # if alarm is turn on or off
    beat = models.IntegerField()
    
    # Notify method
    noti_method = models.CharField( max_length = 8 )
    
    # Other notification options
    noti_email = models.BooleanField(default=True)
    noti_SMS = models.BooleanField(default=False)
    noti_push = models.BooleanField(default=False)
        
    user = models.ForeignKey ( User )
    class Admin:
        pass
    
class NotificationRecord ( models.Model):
    datetime = models.DateTimeField()
    noti_method = models.CharField( max_length = 8 )
    title = models.CharField( max_length = 32 )
    url = models.URLField()
    keyword = models.CharField( max_length = 64)    
    user = models.ForeignKey( User )
    class Admin:
        pass
       
class MonitoringEntry ( models.Model ):
    title = models.CharField ( max_length = 32, unique = True )
    user = models.ForeignKey ( User )
    site = models.ForeignKey ( Site )
    keyword = models.ForeignKey ( Keyword )
    activated = models.BooleanField(default=True)
    
    def __str__ (self):
        return '%s, %s, %s' % ( self.user.username, self.site.url, self.keyword.text)
    
    def get_absolute_url (self):
        return self.site.url
    
    class Admin:
        pass
    
    