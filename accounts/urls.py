from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('username_check/', views.username_check, name='username_check'),
    path('email_check/', views.email_check, name='email_check'),
    path('login/', views.login, name='login'),
]