from django.urls import path

from . import views



urlpatterns = [
    path('',views.wordcloud_view),
]