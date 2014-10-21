import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class RegistrationForm ( forms.Form ):
    username = forms.CharField ( label = 'Username', max_length = 30 )
    email = forms.EmailField ( label = "Email" )
    password1 = forms.CharField ( 
        label = 'Password',
        widget = forms.PasswordInput () ,
        help_text = 'Input your password.'
    )
    
    password2 = forms.CharField ( 
        label = 'Password (again)', 
        widget = forms.PasswordInput ()
     )
    
    def clean_username (self):
        username = self.cleaned_data['username']
        if not re.search( r'^\w+$', username ):
            raise forms.ValidationError ( 'Username can only contain alphanumeric characters and the unserscore.')
        
        try:
            User.objects.get ( username = username )
        except ObjectDoesNotExist:
            return username
            
        raise forms.ValidationError ( 'Username is already taken.' )
    
    def clean_password2 (self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            
            if password1 == password2:
                return password2
            raise forms.ValidationError ( 'Passwords do not match.' )
        
class EntrySaveForm ( forms.Form ):
    title = forms.CharField ( label = 'Title', widget = forms.TextInput ( attrs = { 'size': 32 }))
    url = forms.URLField ( label = 'URL', widget = forms.TextInput ( attrs = { 'size': 128 }))
    keyword = forms.CharField ( label = 'Keyword', widget = forms.TextInput ( attrs = { 'size': 32 }))
    frequency = forms.IntegerField ( label = "Frequency" )
                                    