from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import UploadFeed, Main
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('', Main.as_view(), name='diary'),
    
    path('upload/', UploadFeed.as_view(), name='upload'), 
]



urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)