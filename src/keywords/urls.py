from django.urls import path

from . import views



urlpatterns = [
    path('', views.keywords, name='wordcloud'),   
    path('pop/',views.popular_keywords_view)  
]