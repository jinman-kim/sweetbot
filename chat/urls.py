from django.contrib import admin
from django.urls import path, include
from api import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    path('diary/',include('diary.urls')),
    path('keywords/',include('keywords.urls')),
    path('login/',include('user.urls')),
    path('', views.index, name='index'),
]

