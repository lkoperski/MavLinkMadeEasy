from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register models below

#admin.site.register(User)
admin.site.register(UserPreferences)
admin.site.register(Complete)
admin.site.register(Campus)
admin.site.register(Building)
admin.site.register(Instructor)
admin.site.register(Weekday)
admin.site.register(Offering)
admin.site.register(Course)
admin.site.register(Degree)
admin.site.register(Prereq)
admin.site.register(Requirement)


'''
@DegreeAdmin creates an easily editable form to add
 information to the degree model from the admin page
@param: admin.ModelAdmin representation of a model in the admin interface
@var display 
@var filter
@var fields
'''
#class DegreeAdmin(admin.ModelAdmin):
    #list_display = ('degree', 'major')
    #list_filter = ('degree', 'major')
    #fields = ['degree', 'major', 'req']#

#admin.site.register(Degree, DegreeAdmin)

'''
@CourseAdmin creates an easily editable form to add
 information to the course model from the admin page
@param: admin.ModelAdmin representation of a model in the admin interface
@var display 
@var filter
@var fields
'''
#class CourseAdmin(admin.ModelAdmin):
    #list_display = ('num', 'name', 'special', 'credits')
    #list_filter = ('semester', 'special')
    #search_fields=['prereq__prereq', 'prereq__this_or']
