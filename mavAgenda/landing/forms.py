from django import forms
from .models import *


'''
@EmailForm collection of fields to allow for user login with email address
@forms.Form: associated data within fields
'''
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','password',)

'''
@DegreeForm collection of fields to allow for user to specifiy degree
@forms.Form: associated data within fields
'''
#class DegreeForm(forms.ModelForm):
    #class Meta:
        #model = Degree
        #fields = ('degree',)

'''
@UserForm collection of fields to track user's completed courses
@forms.Form: associated data within fields
'''
#class UserCompletedForm(forms.ModelForm):
    #class Meta:
        #model = Complete
        #fields = ('user', 'complete')
