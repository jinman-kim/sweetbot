from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# a list of all the urls
urlpatterns = [
    path('', views.index, name='index'),
    path('generate_response/', views.generate_response, name='generate_response'),
    path('home/', views.home, name='home'),
    path('new_chat/', views.new_chat, name='new_chat'),
    path('error-handler/', views.error_handler, name='error_handler'),
    path('diary/', views.diary, name='diary'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)