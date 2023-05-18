from django.contrib import admin
from django.urls import path, include
from api import views


urlpatterns = [
<<<<<<< HEAD
    path('', include('api.urls')),
=======
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    path('diary/',include('diary.urls')),
    path('keywords/',include('keywords.urls')),
    path('login/',include('user.urls')),

    path('', views.index, name='index'),
>>>>>>> 0001885d2a98f2836ee22dc5e26525749296cf7a
]

