from django.urls import path
from .views import home, new_chat, error_handler, choose_mbti, mbti_chatbot

urlpatterns = [
    path('', home, name='home'),
    path('new_chat/', new_chat, name='new_chat'),
    path('error-handler/', error_handler, name='error_handler'),
    path('choose_mbti/', choose_mbti, name='choose_mbti'),
    path('mbti_chatbot/<str:prompt>/', mbti_chatbot, name='mbti_chatbot')
]
