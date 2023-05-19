from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


# a list of all the urls
urlpatterns = [
    # 채윤
    path('', views.home, name='home'),
    path('new_chat/', views.new_chat, name='new_chat'),
    path('error-handler/', views.error_handler, name='error_handler'),
    path('choose_mbti/', views.choose_mbti, name='choose_mbti'),
    path('mbti_chatbot/<str:prompt>/', views.mbti_chatbot, name='mbti_chatbot')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)