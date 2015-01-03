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
    
class UserSettings ( models.Model ):
    beat = models.IntegerField()    
    user = models.ForeignKey ( User )
    class Admin:
        pass
       
class MonitoringEntry ( models.Model ):
    title = models.CharField ( primary_key=1, max_length = 32 )
    user = models.ForeignKey ( User )
    site = models.ForeignKey ( Site )
    keyword = models.ForeignKey ( Keyword )
    
    def __str__ (self):
        return '%s, %s, %s' % ( self.user.username, self.site.url, self.keyword.text)
    
    def get_absolute_url (self):
        return self.site.url
    
    class Admin:
        pass
    
    