from django.urls import path, include
# here we are importing all the Views from the views.py file
from . import views

# a list of all the urls
urlpatterns = [
    path('', views.home, name='home'),
    path('new_chat/', views.new_chat, name='new_chat'),
    path('error-handler/', views.error_handler, name='error_handler'),
    path('choose_mbti/', views.choose_mbti, name='choose_mbti'),
    path('mbti_chatbot/', views.mbti_chatbot, name='mbti_chatbot'),
]