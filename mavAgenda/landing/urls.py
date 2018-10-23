from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'landing'
urlpatterns = [
    path('', views.login, name='login'),
    path('selectcourses/<int:pk>', views.selectcourses, name='selectcourses'),
    path('nextsemesterpreferences/<int:pk>', views.nextsemesterpreferences, name='nextsemesterpreferences'),
    path('schedule/<int:pk>', views.schedule, name='schedule'),
    path('createuser/', views.createuser, name='createuser'),
]
