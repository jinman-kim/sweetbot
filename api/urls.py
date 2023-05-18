<<<<<<< HEAD
from django.urls import path, include
# here we are importing all the Views from the views.py file
=======
from django.urls import path
>>>>>>> 0001885d2a98f2836ee22dc5e26525749296cf7a
from . import views
from django.conf import settings
from django.conf.urls.static import static



# a list of all the urls
urlpatterns = [
    #path('', views.index, name='index'),
    path('generate_response/', views.generate_response, name='generate_response'),
    path('', views.home, name='home'),
    path('', views.new_chat, name='new_chat'),
    path('error-handler/', views.error_handler, name='error_handler'),
<<<<<<< HEAD
    path('choose_mbti/', views.choose_mbti, name='choose_mbti'),
    path('mbti_chatbot/', views.mbti_chatbot, name='mbti_chatbot'),
]
=======
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 0001885d2a98f2836ee22dc5e26525749296cf7a
