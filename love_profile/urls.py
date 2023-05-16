from django.urls import path

from . import views



urlpatterns = [
    path('',views.love_profile,name='diary'),    
]