from django.urls import path
from .views import Login, Join
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('join/', Join.as_view(), name='join'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
