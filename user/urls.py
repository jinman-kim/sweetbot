from django.urls import path
from .views import Login, Join


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('', Join.as_view(), name='join'),
]
