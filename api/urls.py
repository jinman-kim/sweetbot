from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import UploadFeed, Main

# a list of all the urls
urlpatterns = [
    path('', views.index, name='index'),
    path('generate_response/', views.generate_response, name='generate_response'),
    path('home/', views.home, name='home'),
    path('new_chat/', views.new_chat, name='new_chat'),
    path('error-handler/', views.error_handler, name='error_handler'),
    path('diary/', Main.as_view(), name='diary'),
    path('diary/upload/', UploadFeed.as_view(), name='upload'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)